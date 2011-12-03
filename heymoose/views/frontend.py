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
import base64

from flask import Module
from heymoose.utils.decorators import auth_only, role_not_detected_only, admin_only
from heymoose.utils.workers import app_logger, heymoose_app
from heymoose.utils.shortcuts import do_or_abort
from heymoose.core.actions import apps, roles
from heymoose import config
import heymoose.forms.forms as forms
import heymoose.core.actions.users as users

frontend = Module(__name__)
from heymoose.views.facebook_app.facebook import *
from heymoose.views.facebook_app.oauth import *
from heymoose.views.facebook_app.callback import *
from heymoose.views.vkontakte import *
from heymoose.views.offer import *
from heymoose.views.action import *
from heymoose.views.work import *
from heymoose.views.balance import *
from heymoose.views.blog import *
from heymoose.views.developer import *
from heymoose.views.customer import *
from heymoose.views.app import *
from heymoose.views.order import *
from heymoose.views.gifts import *
from heymoose.views.info import *
from heymoose.views.survey import *
from heymoose.tests.postgress_stres_test import *

from heymoose.db.actions import captcha, invites

def register_form_template(form_params=None, error=None):
	register_form = forms.RegisterForm()
	if form_params:
		register_form.username.data = form_params['username']
		register_form.email.data = form_params['email']
		register_form.password.data = form_params['password']
		register_form.password2.data = form_params['password2']

	g.params['captcha'] = captcha.get_random()
	g.params['registerform'] = register_form
	return render_template('new_register.html', params=g.params, error=error)

@frontend.route('/')
def main_page():
	g.params['loginform'] = forms.LoginForm()
	#return render_template('index.html', params=g.params)
	return render_template('new_index.html', params=g.params)

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
			users.add_user_role(user_id=g.user.id, role=form_role.role.data)
			return redirect(url_for('cabinet.index'))
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
			flash_form_errors([['Извините, попробуйте еще раз']], 'roleerror')
			
	g.params['roleform'] = form_role 
	flash_form_errors([['Извините, попробуйте еще раз']], 'roleerror')
	return render_template('new-role-selection.html', params=g.params)



@frontend.route('/start_survey')
@auth_only
def start_survey():
	return redirect(url_for('user_cabinet'))

'''
@frontend.route('/cabinet')
@auth_only
def user_cabinet():
    if g.user is None:
        abort(403)
        
    if g.user.is_admin():
        return redirect(url_for('admin.index'))

    if g.user.is_developer():
        return redirect(url_for('cabinet_apps'))
        
    if g.user.is_customer():
        return redirect(url_for('cabinet_orders'))
    
    app_loger.error("Shit happened user has unknown role in user_cabinet")
    abort(404)

@frontend.route('/cabinet/info')
@auth_only
def cabinet_info():
    return render_template('new-cabinet-info.html')
'''
@frontend.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""

	if g.user:
		return redirect(url_for('main_page'))

	form_login = forms.LoginForm(request.form)
	if request.method == 'POST' and form_login.validate():
		user = users.get_user_by_email(form_login.username.data)
		if user is None or not check_password_hash(user.password_hash, form_login.password.data):
			flash(u'Неверный логин или пароль', 'error')
		else:
			session['user_id'] = user.id
			return redirect(url_for('cabinet.index'))

	return redirect(url_for('main_page'))


@frontend.route('/register', methods=['GET', 'POST'])
def register():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('main_page'))
	
	form = forms.DeveloperRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(users.add_user,
			email=form.email.data,
			passwordHash=generate_password_hash(form.password.data),
			nickname=form.username.data)
		user = do_or_abort(users.get_user_by_email, form.email.data, full=True)
		if user:
			users.add_user_role(user.id, roles.DEVELOPER)
			invites.register_invite(form.invite.data)
			session['user_id'] = user.id
			flash(u'Вы успешно зарегистрированы', 'success')
			return redirect(url_for('cabinet.index'))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
		
	return render_template('new_register.html', form=form)
		
	

'''
@frontend.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('main_page'))
    error = None
    register_form = forms.RegisterForm(request.form)
    if request.method == 'POST' and register_form.validate():
        if register_form.password.data != register_form.password2.data:
            flash_form_errors([[u'Введенные пароли не совпадают']], 'registererror')
        elif users.get_user_by_email(register_form.email.data) is not None:
            flash_form_errors([[u'Введенный email уже используется']], 'registererror')
        # Уязвимость, данные из поля капча и hidden не проверяются.
        elif captcha.check_captcha(request.form['captcha_id'], register_form.captcha.data) is None:
            flash_form_errors([[u'Капча не верна, попробуйте еще раз']], 'registererror')
        else:
            users.add_user(email=register_form.email.data,
                            passwordHash=generate_password_hash(register_form.password.data),
                            nickname=register_form.username.data)

            #request user and loged him in
            user = users.get_user_by_email(register_form.email.data, full=True)
            if user:
                users.add_user_role(user.id, register_form.role.data)
                session['user_id'] = user.id
                return redirect(url_for('cabinet.index'))
    
    flash_form_errors(register_form.errors.values(), 'registererror')
    return register_form_template(request.form, error)
'''

@frontend.route('/logout')
@role_not_detected_only
def logout():
	"""Logs the user out."""
	flash(u'Вы вышли из системы', 'info')
	session.pop('user_id', None)
	return redirect(url_for('main_page'))

if __name__ == '__main__':
	app.run()
