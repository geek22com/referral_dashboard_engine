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
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.db.models import User
from heymoose.db.models import Captcha
import heymoose.forms.forms as forms

frontend = Module(__name__)
from heymoose.views.work import *
from heymoose.views.balance import *
from heymoose.views.blog import *
from heymoose.views.developer import *
from heymoose.views.order import *
from heymoose.views.info import *
from heymoose.tests.postgress_stres_test import *

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

@frontend.route('/start_survey')
@auth_only
def start_survey():
	#return render_template('cabinet-inside-service.html', params=g.params)
	return redirect(url_for('user_cabinet', username=g.user.username))

@frontend.route('/<username>')
@auth_only
def user_cabinet(username):
	if g.user is None:
		abort(404)

	developer_profile = Developer.get_developer(g.user.userid)
	if developer_profile:
		g.params['app_id'] = developer_profile.app_id
		g.params['secret_key'] = developer_profile.secret_key

	orders = Order.load_orders(g.user.userid, 0)
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
		user = User.get_user(form_login.username.data)
		if user is None:
			flash_form_errors([['Такой пользователь не зарегистрирован']], 'loginerror')
		elif not check_password_hash(user.passwordhash, form_login.password.data):
			flash_form_errors([['Неверный пароль']], 'loginerror')
		else:
			session['user_id'] = user.userid
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
		elif Captcha.check_captcha(request.form['captcha_id'], request.form['captcha_answer']) is None:
			flash_form_errors([['Каптча введена не верна']], 'registererror')
		else:
			try:
				user = User(username=register_form.username.data,
							email=register_form.email.data,
							passwordhash=generate_password_hash(register_form.password.data))
				user.save()

				#request user and loged him in
				user = User.get_user(register_form.username.data)
				if user:
					session['user_id'] = user.userid
				else:
					redirect(url_for('register_success'))
			except:
				flash_form_errors([['Извините, регистрация временно не доступна']], 'registererror')

			return redirect(url_for('user_cabinet', username=user.username))

	flash_form_errors(register_form.errors.values(), 'registererror')
	return register_form_template(request.form, error)

@frontend.route('/logout')
@auth_only
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('main_page'))


# add some filters to jinja
#app.jinja_env.filters['datetimeformat'] = format_datetime
#app.jinja_env.filters['gravatar'] = gravatar_url


if __name__ == '__main__':
    app.run()

############################ Profiling, Must be removed in production ##########################################

