# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, request, flash, session, abort
from heymoose import app
from heymoose.site import blueprint as bp
from heymoose.forms import forms
from heymoose.utils.gen import generate_password_hash, check_password_hash, aes_base16_decrypt
from heymoose.utils.shortcuts import do_or_abort
from heymoose.core.actions import users, roles
from heymoose.db.models import Contact, GamakApp
from heymoose.db.actions import invites
from heymoose.mail import marketing as mmail
from heymoose.mail import transactional as tmail
from datetime import datetime
import random


@bp.route('/')
def index():
	return render_template('site/index.html')


#@bp.route('/about')
def about():
	'''Deprecated'''
	return render_template('site/about.html')

@bp.route('/customers')
def customers():
	return render_template('site/to-customer.html')

@bp.route('/developers')
def developers():
	return render_template('site/to-developer.html')

@bp.route('/platforms')
def platforms():
	return render_template('site/platforms.html')


@bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
	form = forms.ContactForm(request.form)
	if request.method == 'POST' and form.validate():
		contact = Contact(date=datetime.now(), partner=False)
		form.populate_obj(contact)
		contact.save()
		tmail.admin_feedback_added(contact)
		flash(u'Спасибо, мы обязательно с вами свяжемся!', 'success')
		return redirect(url_for('.contacts'))
	return render_template('site/contacts.html', form=form)

@bp.route('/partner', methods=['GET', 'POST'])
def contacts_partner():
	form = forms.PartnerContactForm(request.form)
	if request.method == 'POST' and form.validate():
		contact = Contact(date=datetime.now(), partner=True)
		form.populate_obj(contact)
		contact.save()
		tmail.admin_feedback_added(contact)
		flash(u'Спасибо, мы обязательно с вами свяжемся!', 'success')
		return redirect(url_for('.index'))
	return render_template('site/contacts-partner.html', form=form)


@bp.route('/register/')
def register():
	ref = request.args.get('ref', None)
	if ref:
		session['ref'] = ref
		return redirect(url_for('.register_customer'))
	
	return render_template('site/register.html')

@bp.route('/register/developer', methods=['GET', 'POST'])
def register_developer():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('.index'))
	
	form = forms.DeveloperRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		users.add_user(
			email=form.email.data,
			password_hash=generate_password_hash(form.password.data),
			first_name=form.first_name.data,
			last_name=form.last_name.data,
			organization=form.organization.data,
			phone=form.phone.data,
			messenger_type=form.messenger_type.data,
			messenger_uid=form.messenger_uid.data)
		user = users.get_user_by_email(form.email.data, full=True)
		if user:
			users.confirm_user(user.id)
			mmail.lists_add_user(user)
			users.add_user_role(user.id, roles.DEVELOPER)
			user.roles.append(roles.DEVELOPER)
			invites.register_invite(form.invite.data)
			session['user_id'] = user.id
			flash(u'Вы успешно зарегистрированы', 'success')
			return redirect(url_for('cabinet.index'))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
		
	return render_template('site/register-developer.html', form=form)

@bp.route('/register/customer', methods = ['GET', 'POST'])
def register_customer():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('.index'))
	
	ref = session.get('ref', '')
	key = app.config.get('REFERRAL_CRYPT_KEY', 'qwertyui12345678')
	
	try:
		id, _salt = aes_base16_decrypt(key, ref).split('$')
		referrer = users.get_user_by_id(int(id))
		if not referrer or not referrer.is_customer():
			raise ValueError()
	except:
		form = None
	else:
		form = forms.CustomerRegisterForm(request.form)
		if request.method == 'POST' and form.validate():
			users.add_user(email=form.email.data,
				password_hash=generate_password_hash(form.password.data),
				first_name=form.first_name.data,
				last_name=form.last_name.data,
				organization=form.organization.data,
				phone=form.phone.data,
				messenger_type=form.messenger_type.data,
				messenger_uid=form.messenger_uid.data,
				referrer_id=referrer.id)
			user = users.get_user_by_email(form.email.data, full=True)
			if user:
				users.add_user_role(user.id, roles.CUSTOMER)
				user.roles.append(roles.CUSTOMER)
				session['user_id'] = user.id
				session['ref'] = ''
				tmail.user_confirm_email(user)
				flash(u'Вы успешно зарегистрированы. На указанный электронный адрес'
					u' было выслано письмо с подтверждением.', 'success')
				return redirect(url_for('cabinet.index'))
			flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
	
	return render_template('site/register-customer.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
	if g.user: return redirect(url_for('.index'))

	form = forms.LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = users.get_user_by_email(form.username.data)
		if user is None or not check_password_hash(user.password_hash, form.password.data):
			flash(u'Неверный e-mail или пароль', 'error')
		else:
			session['user_id'] = user.id
			session.permanent = form.remember.data
			return redirect(request.args.get('back', None) or url_for('cabinet.index'))
	return render_template('site/login.html', form=form)


@bp.route('/logout')
def logout():
	if g.user:
		flash(u'Вы вышли из системы', 'info')
		session.pop('user_id', None)
		session.permanent = False
	return redirect(url_for('.index'))


@bp.route('/confirm/<int:id>/<code>')
def confirm(id, code):
	user = do_or_abort(users.get_user_by_id, id)
	success = False
	if user.check_confirm_code(code):
		users.confirm_user(user.id)
		mmail.lists_add_user(user)
		success = True
	return render_template('site/confirm.html', success=success)


@bp.route('/gamak/')
def gamak():
	return render_template('site/gamak.html')

@bp.route('/gamak/apps/')
def gamak_apps():
	if not g.user or not g.user.is_admin(): abort(403)
	aps = GamakApp.query.filter(GamakApp.active == True).all()
	random.shuffle(aps)
	return render_template('site/gamak-apps.html', apps=aps)

