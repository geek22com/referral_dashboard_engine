# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, request, flash, session
from heymoose.site import blueprint as bp
from heymoose.forms import forms
from heymoose.utils.shortcuts import do_or_abort
from heymoose.utils.gen import generate_password_hash, check_password_hash
from heymoose.core.actions import users, roles
from heymoose.db.actions import invites


@bp.route('/')
def index():
	return render_template('site/index.html')


@bp.route('/about')
def about():
	return render_template('site/about.html')


@bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
	form = forms.ContactForm(request.form)
	'''if request.method == 'POST' and contact_form.validate():
		if captcha.check_captcha(request.form['captcha_id'], contact_form.captcha_answer.data) is None:
			flash_form_errors([['Каптча введена не верно']], 'contactinfoerror')
		else:
		    contact = Contact(
				name = contact_form.name.data,
				email = contact_form.email.data,
				phone = contact_form.phone.data,
				desc = contact_form.comment.data)
			contact.save()
			flash_form_errors([["Спасибо, мы обязательно с вами свяжемся"]], 'contactinfoerror')
			return redirect(url_for('contacts'))
	flash_form_errors(contact_form.errors.values(), 'contactinfoerror')'''
	return render_template('site/contacts.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('.index'))
	
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
		
	return render_template('site/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if g.user: return redirect(url_for('.index'))

	form = forms.LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = users.get_user_by_email(form.username.data)
		if user is None or not check_password_hash(user.password_hash, form.password.data):
			flash(u'Неверный логин или пароль', 'error')
		else:
			session['user_id'] = user.id
			return redirect(url_for('cabinet.index'))

	return redirect(url_for('.index'))


@bp.route('/logout')
def logout():
	if g.user:
		flash(u'Вы вышли из системы', 'info')
		session.pop('user_id', None)
	return redirect(url_for('.index'))

