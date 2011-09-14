# -*- coding: utf-8 -*-
"""
    heymoose.com frontend
    ~~~~~~~~
"""
from __future__ import with_statement
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash
import random
import string
import sys
import profiling

from flask import Module
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import role_not_detected_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.utils.workers import heymoose_app
from heymoose.db.models import User
from heymoose.db.models import Captcha
import heymoose.settings.debug_config as config
import heymoose.forms.forms as forms

frontend = Module(__name__)
from heymoose.views.facebook import *
from heymoose.views.vkontakte import *
from heymoose.views.offer import *
from heymoose.views.work import *
from heymoose.views.balance import *
from heymoose.views.blog import *
from heymoose.views.developer import *
from heymoose.views.customer import *
from heymoose.views.app import *
from heymoose.views.order import *
from heymoose.views.info import *
from heymoose.views.survey import *
from heymoose.tests.postgress_stres_test import *
import heymoose.db.resource_user as resource_user

def register_form_template(form_params=None, error=None):
	register_form = forms.RegisterForm()
	if form_params:
		register_form.username.data = form_params['username']
		register_form.email.data = form_params['email']
		register_form.password.data = form_params['password']
		register_form.password2.data = form_params['password2']

	g.params['captcha'] = Captcha.get_random()
	g.params['registerform'] = register_form
	return render_template('register.html', params=g.params, error=error)

@frontend.route('/')
def main_page():
	g.params['loginform'] = forms.LoginForm()
	return render_template('index.html', params=g.params)

@frontend.route('/register_success')
def register_success():
	g.params['loginform'] = forms.LoginForm()
	return render_template('register_success.html', params=g.params)

@frontend.route('/role_detect', methods=['GET', 'POST'])
@role_not_detected_only
def role_detect():
	form_role = forms.RoleForm(request.form)
	if request.method == 'POST' and form_role.validate():
		try:
			if not g.user:
				raise Exception()

			g.user.set_roles(resource_user.create_role(form_role.role.data))
			return redirect(url_for('user_cabinet', username=g.user.nickname))
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
			flash_form_errors([['Извините, попробуйте еще раз']], 'roleerror')

	flash_form_errors([['Извините, попробуйте еще раз']], 'roleerror')
	return render_template('role-selection.html', params=g.params)



@frontend.route('/start_survey')
@auth_only
def start_survey():
	return redirect(url_for('user_cabinet', username=g.user.nickname))

@frontend.route('/<username>')
@auth_only
def user_cabinet(username):
	print "user_cabinet " + str(username)
	if g.user is None:
		abort(404)

	if g.user.is_developer():
		apps = g.user.get_apps()
		if apps:
			g.params['apps'] = apps

	if g.user.is_customer():
		orders = g.user.get_orders()
		if orders:
			g.params['orders'] = orders
	return render_template('cabinet-inside-service.html', params=g.params)


@frontend.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""

	if g.user:
		return redirect(url_for('main_page'))

	form_login = forms.LoginForm(request.form)
	if request.method == 'POST' and form_login.validate():
		#user = User.get_user(form_login.username.data)
		user = User.get_user_by_email(form_login.username.data)
		if user is None:
			flash_form_errors([['Такой пользователь не зарегистрирован']], 'loginerror')
		elif not check_password_hash(user.passwordHash, form_login.password.data):
			flash_form_errors([['Неверный логин или пароль']], 'loginerror')
		else:
			session['user_id'] = user.id
			return redirect(url_for('user_cabinet', username=form_login.username.data))

	flash_form_errors(form_login.errors.values(), 'loginerror')
	return redirect(url_for('main_page'))

@frontend.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('main_page'))
	error = None
	register_form = forms.RegisterForm(request.form)
	if request.method == 'POST' and register_form.validate():
		if register_form.password.data != register_form.password2.data:
			flash_form_errors([['Введенные пароли не совпадают']], 'registererror')
		elif User.check_user(register_form.email.data) is not None:
			flash_form_errors([['Введенный email уже используется']], 'registererror')
		# Уязвимость, данные из поля капча и hidden не проверяются.
		elif config.USE_DATABASE and Captcha.check_captcha(request.form['captcha_id'], request.form['captcha_answer']) is None:
			flash_form_errors([['Каптча введена не верна']], 'registererror')
		else:
			try:
				user = User(nickname=register_form.username.data,
							email=register_form.email.data,
							passwordHash=generate_password_hash(register_form.password.data),
							roles=resource_user.create_role(register_form.role.data))
				user.save()
				#request user and loged him in
				user = User.get_user_by_email(register_form.email.data)
				if user:
					user.set_roles(resource_user.create_role(register_form.role.data))
					session['user_id'] = user.id
				else:
					#return redirect(url_for('register_success'))
					raise Exception()

				return redirect(url_for('user_cabinet', username=user.nickname))
			except Exception as inst:
				app_logger.error(inst)
				app_logger.error(sys.exc_info())
				flash_form_errors([['Извините, регистрация временно не доступна']], 'registererror')

	flash_form_errors(register_form.errors.values(), 'registererror')
	return register_form_template(request.form, error)

@frontend.route('/logout')
@role_not_detected_only
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('main_page'))

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
	return value.strftime(format)

# add some filters to jinja
heymoose_app.jinja_env.filters['datetimeformat'] = datetimeformat
#app.jinja_env.filters['gravatar'] = gravatar_url


if __name__ == '__main__':
    app.run()

############################ Profiling, Must be removed in production ##########################################

