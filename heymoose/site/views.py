# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, request, flash, session, jsonify, abort
from heymoose import app, resource as rc
from heymoose.site import blueprint as bp
from heymoose.forms import forms
from heymoose.utils.gen import check_password_hash
from heymoose.views.decorators import template
from heymoose.db.models import Contact
from heymoose.mail import marketing as mmail, transactional as tmail
from heymoose.data.models import User
from heymoose.data.enums import Roles
from heymoose.data.repos import regions_repo
from datetime import datetime


@bp.route('/')
@template('site/ak/index.html')
def index():
	confirmed = request.args.get('confirmed')
	if confirmed == '1':
		flash(u'Ваш адрес электронной почты успешно подтвержден', 'success')
	elif confirmed == '0':
		flash(u'Ошибка при подтверждении адреса электронной почты', 'success')
	return dict(
		form=forms.AffiliateRegisterForm(),
		offer_count=rc.pub.offer_count(),
		top_withdrawals=rc.pub.top_withdrawals(),
		top_conversion=rc.pub.top_conversion()
	)

@bp.route('/advertisers/')
@template('site/ak/advertisers.html')
def advertisers():
	return dict(form=forms.AdvertiserRegisterForm())

@bp.route('/affiliates/')
@template('site/ak/affiliates.html')
def affiliates():
	return dict(form=forms.AffiliateRegisterForm())

@bp.route('/<any(en,de,fr,it):lang>/')
def lang_index(lang):
	return render_template('site/hm/{0}/index.html'.format(lang), lang=lang)

@bp.route('/<any(en,de,fr,it):lang>/advertisers/')
def lang_advertisers(lang):
	return render_template('site/hm/{0}/advertisers.html'.format(lang), lang=lang)

@bp.route('/<any(en,de,fr,it):lang>/affiliates/')
def lang_affiliates(lang):
	return render_template('site/hm/{0}/affiliates.html'.format(lang), lang=lang)

@bp.route('/contacts/', methods=['GET', 'POST'])
@template('site/ak/contacts.html')
def contacts():
	form = forms.ContactForm(request.form)
	if request.method == 'POST' and form.validate():
		contact = Contact(date=datetime.now(), partner=False)
		form.populate_obj(contact)
		contact.save()
		tmail.admin_feedback_added(contact)
		flash(u'Спасибо, мы обязательно с вами свяжемся!', 'success')
		return redirect(url_for('.contacts'))
	return dict(form=form)

@bp.route('/gateway/')
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

@bp.route('/register/advertiser/', methods=['GET', 'POST'])
@template('site/ak/register-advertiser.html')
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
	return dict(form=form)
			

@bp.route('/register/affiliate/', methods=['GET', 'POST'])
@template('site/ak/register-affiliate.html')
def register_affiliate():
	if g.user:
		flash(u'Вы уже зарегистрированы', 'warning')
		return redirect(url_for('.index'))
	
	form = forms.AffiliateRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User()
		form.populate_obj(user)
		ref = request.args.get('ref', '')
		referrer_id = User.get_referrer_id(ref)
		referrer = rc.users.get_by_id_safe(referrer_id) if referrer_id else None
		if referrer and referrer.is_affiliate:
			user.referrer = referrer_id
		rc.users.add(user)
		user = rc.users.get_by_email_safe(user.email)
		if user:
			rc.users.add_role(user.id, Roles.AFFILIATE)
			user.roles.append(Roles.AFFILIATE)
			session['user_id'] = user.id
			session['ref'] = ''
			tmail.user_confirm_email(user)
			flash(u'Вы успешно зарегистрированы. На указанный электронный адрес'
				u' было выслано письмо с подтверждением.', 'success')
			return redirect(url_for('.gateway'))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
	return dict(form=form)

@bp.route('/login/', methods=['GET', 'POST'])
@template('site/ak/login.html')
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
	return dict(form=form)

@bp.route('/logout/')
def logout():
	if g.user:
		flash(u'Вы вышли из системы', 'info')
		session.pop('user_id', None)
		session.permanent = False
	return redirect(url_for('.index'))

@bp.route('/password/', methods=['GET', 'POST'])
@template('site/ak/password.html')
def password():
	if g.user:
		return redirect(url_for('.index'))
	
	form = forms.ForgottenPasswordForm(request.form)
	if request.method == 'POST' and form.validate():
		user = rc.users.get_by_email_safe(form.email.data)
		if user is not None and not user.is_admin:
			new_password = user.generate_password()
			rc.users.update(user)
			tmail.user_restore_password(user, new_password)
			flash(u'Новый пароль выслан на указанный электронный адрес', 'success')
			return redirect(url_for('.index'))
		else:
			flash(u'Неверный e-mail', 'error')
	return dict(form=form)

@bp.route('/confirm/<int:id>/<code>')
def confirm(id, code):
	user = rc.users.get_by_id(id)
	if user.check_confirm_code(code):
		rc.users.confirm(user.id)
		mmail.lists_add_user(user)
		return redirect(url_for('.index', confirmed=1))
	return redirect(url_for('.index', confirmed=0))

@bp.route('/catalog/')
@template('site/ak/catalog.html')
def catalog(**kwargs):
	regions = regions_repo.as_list()
	return dict(regions=regions)

@bp.route('/catalog/page/')
def catalog_page():
	form = forms.CatalogOfferFilterForm(request.args)
	if form.validate():
		offers, _ = rc.offers.list(approved=True, active=True, launched=True, showcase=True, **form.backend_args())
		json_offers = []
		for offer in offers:
			json_offers.append(dict(
				id=offer.id,
				link=url_for('.catalog_offer', id=offer.id),
				name=offer.name,
				short_description=offer.short_description,
				logo=url_for('upload', filename=offer.logo) if offer.logo_filename else None,
				title=offer.title,
				value=offer.value(affiliate=True, short=True).split(u'и')[0],
				regions=u', '.join([r.country_name for r in offer.regions_full]),
				exclusive=offer.exclusive,
				more_suboffers=bool(offer.active_suboffers)
			))
		return jsonify(offers=json_offers)
	return 'Bad request', 400

@bp.route('/catalog/<int:id>/')
@template('site/ak/catalog-offer.html')
def catalog_offer(id):
	offer = rc.offers.get_by_id(id)
	if not offer.visible: abort(404)
	return dict(offer=offer)
