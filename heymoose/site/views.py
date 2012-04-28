# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, request, flash, session, abort
from heymoose import app
from heymoose.site import blueprint as bp
from heymoose.forms import forms
from heymoose.utils.gen import check_password_hash
from heymoose.db.models import Contact
from heymoose.mail import marketing as mmail, transactional as tmail
from heymoose.data.models import User
from heymoose.data.enums import Roles
from heymoose import resource as rc
from datetime import datetime


@bp.route('/')
def index():
	return render_template('site/index.html')

@bp.route('/cpa/')
def cpa_index():
	return redirect(url_for('.index'))

@bp.route('/advertisers')
def advertisers():
	return render_template('site/advertisers.html')

@bp.route('/affiliates')
def affiliates():
	return render_template('site/affiliates.html')

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

@bp.route('/gateway')
def gateway():
	if not g.user:
		return redirect(url_for('.index'))
	elif g.user.is_admin:
		return redirect(url_for('admin.index'))
	elif g.user.is_affiliate or g.user.is_advertiser:
		return redirect(url_for('cabinetcpa.index'))
	else:
		app.logger.error('Shit happened: registered user has unknown role')
		return redirect(url_for('.index'))

@bp.route('/register/')
def register():
	return render_template('site/register.html')

@bp.route('/register/advertiser', methods=['GET', 'POST'])
def register_advertiser():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('.index'))
	
	form = forms.AdvertiserRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User()
		form.populate_obj(user)
		rc.users.add(user)
		user = rc.users.get_by_email_safe(user.email)
		if user:
			rc.users.add_role(user.id, Roles.ADVERTISER)
			user.roles.append(Roles.ADVERTISER)
			session['user_id'] = user.id
			tmail.user_confirm_email(user)
			flash(u'Вы успешно зарегистрированы. На указанный электронный адрес'
				u' было выслано письмо с подтверждением.', 'success')
			return redirect(url_for('.gateway'))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
	return render_template('site/register-advertiser.html', form=form)
			

@bp.route('/register/affiliate', methods=['GET', 'POST'])
def register_affiliate():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('.index'))
	
	form = forms.AffiliateRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User()
		form.populate_obj(user)
		rc.users.add(user)
		user = rc.users.get_by_email_safe(user.email)
		if user:
			rc.users.add_role(user.id, Roles.AFFILIATE)
			user.roles.append(Roles.AFFILIATE)
			session['user_id'] = user.id
			tmail.user_confirm_email(user)
			flash(u'Вы успешно зарегистрированы. На указанный электронный адрес'
				u' было выслано письмо с подтверждением.', 'success')
			return redirect(url_for('.gateway'))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
	return render_template('site/register-affiliate.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
	if g.user:
		return redirect(url_for('.index'))

	form = forms.LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = rc.users.get_by_email_safe(form.username.data)
		if user is None or not check_password_hash(user.password_hash, form.password.data):
			flash(u'Неверный e-mail или пароль', 'error')
		else:
			session['user_id'] = user.id
			session.permanent = form.remember.data
			return redirect(request.args.get('back', None) or url_for('.gateway'))
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
	user = rc.users.get_by_id(id)
	success = False
	if user.check_confirm_code(code):
		rc.users.confirm(user.id)
		mmail.lists_add_user(user)
		success = True
	return render_template('site/confirm.html', success=success)


###

@bp.route('/news/<name>')
def news_item(name):
	try:
		return render_template('site/news/{0}.html'.format(name))
	except:
		abort(404)

@bp.route('/special/<name>')
def special(name):
	try:
		return render_template('site/hm/special-{0}.html'.format(name))
	except:
		abort(404)

@bp.route('/new/')
def new_index():
	if not g.user or not g.user.is_admin: abort(403)
	return render_template('site/hm/index.html')

@bp.route('/new/advertisers')
def new_advertisers():
	if not g.user or not g.user.is_admin: abort(403)
	return render_template('site/hm/advertisers.html')

@bp.route('/new/advertisers/cpa')
def new_advertisers_cpa():
	if not g.user or not g.user.is_admin: abort(403)
	return render_template('site/hm/advertisers-cpa.html')

@bp.route('/new/affiliates')
def new_affiliates():
	if not g.user or not g.user.is_admin: abort(403)
	return render_template('site/hm/affiliates.html')

@bp.route('/new/contacts')
def new_contacts():
	if not g.user or not g.user.is_admin: abort(403)
	form = forms.ContactForm()
	return render_template('site/hm/contacts.html', form=form)

@bp.route('/new/register/advertiser')
def new_register_advertiser():
	if not g.user or not g.user.is_admin: abort(403)
	form = forms.AdvertiserRegisterForm(request.form)
	return render_template('site/hm/register-advertiser.html', form=form)

@bp.route('/new/register/affiliate')
def new_register_affiliate():
	if not g.user or not g.user.is_admin: abort(403)
	form = forms.AffiliateRegisterForm(request.form)
	return render_template('site/hm/register-affiliate.html', form=form)

@bp.route('/catalog/')
def catalog():
	if not g.user or not g.user.is_admin: abort(403)
	return render_template('site/hm/catalog.html')
