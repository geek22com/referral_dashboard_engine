# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, request, flash, session, abort
from heymoose import app
from heymoose.site import blueprint as bp
from heymoose.forms import forms
from heymoose.utils.gen import check_password_hash
from heymoose.utils.convert import to_unixtime
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.views.decorators import template
from heymoose.db.models import Contact, NewsItem
from heymoose.mail import marketing as mmail, transactional as tmail
from heymoose.data.models import User
from heymoose.data.enums import Roles
from heymoose import resource as rc
from datetime import datetime


@bp.route('/')
def index():
	news = NewsItem.query.filter(
		NewsItem.active == True,
		NewsItem.on_main == True
	).descending(NewsItem.date).limit(6)
	return render_template('site/hm/index.html', news=news)

@bp.route('/cpa/')
def cpa_index():
	return redirect(url_for('.index'))

@bp.route('/advertisers')
def advertisers():
	return render_template('site/hm/advertisers.html')

@bp.route('/affiliates')
def affiliates():
	return render_template('site/hm/affiliates.html')

@bp.route('/en/')
@template('site/hm/en/index.html')
def en_index(): return {}

@bp.route('/en/advertisers/')
@template('site/hm/en/advertisers.html')
def en_advertisers(): return {}

@bp.route('/en/affiliates/')
@template('site/hm/en/affiliates.html')
def en_affiliates(): return {}

@bp.route('/affiliates/contest')
def affiliates_contest():
	kwargs = {
		'from': to_unixtime(datetime(2012, 6, 18), msec=True),
		'to': to_unixtime(datetime(2012, 8, 31), msec=True),
		'offset': 0,
		'limit' : 50
	}
	stats = rc.offer_stats.list_affiliate_top(**kwargs)
	return render_template('site/hm/affiliates-contest.html', stats=stats)

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
	return render_template('site/hm/contacts.html', form=form)

@bp.route('/job')
def job():
	return render_template('site/hm/job.html')

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
	return render_template('site/hm/register-advertiser.html', form=form)
			

@bp.route('/register/affiliate', methods=['GET', 'POST'])
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
	return render_template('site/hm/register-affiliate.html', form=form)

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
	return render_template('site/hm/login.html', form=form)


@bp.route('/logout')
def logout():
	if g.user:
		flash(u'Вы вышли из системы', 'info')
		session.pop('user_id', None)
		session.permanent = False
	return redirect(url_for('.index'))

@bp.route('/password', methods=['GET', 'POST'])
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
			return redirect(url_for('.login'))
		else:
			flash(u'Неверный e-mail', 'error')
	return render_template('site/hm/password.html', form=form)


@bp.route('/confirm/<int:id>/<code>')
def confirm(id, code):
	user = rc.users.get_by_id(id)
	success = False
	if user.check_confirm_code(code):
		rc.users.confirm(user.id)
		mmail.lists_add_user(user)
		success = True
	return render_template('site/hm/confirm.html', success=success)

@bp.route('/news/')
def news_list():	
	page = current_page()
	per_page = 10
	offset, limit = page_limits(page, per_page)
	news = NewsItem.query.filter(NewsItem.active == True).descending(NewsItem.date).skip(offset).limit(limit)
	count = NewsItem.query.filter(NewsItem.active == True).count()
	pages = paginate(page, count, per_page)
	return render_template('site/hm/news.html', news=news.all(), pages=pages)
		
@bp.route('/news/<id>')
def news_item(id):
	newsitem = NewsItem.query.get(id)
	if not newsitem.active:
		abort(404)
	news = NewsItem.query.filter(
		NewsItem.mongo_id != newsitem.mongo_id,
		NewsItem.active == True
	).descending(NewsItem.date).limit(2)
	return render_template('site/hm/newsitem.html', newsitem=newsitem, news=news)

@bp.route('/special/<name>')
def special(name):
	try:
		return render_template('site/hm/special-{0}.html'.format(name))
	except:
		abort(404)

@bp.route('/advertisers/cpa')
def advertisers_cpa():
	return render_template('site/hm/advertisers-cpa.html')

@bp.route('/catalog/')
def catalog():
	page = current_page()
	per_page = app.config.get('OFFERS_PER_PAGE', 10)
	offset, limit = page_limits(page, per_page)
	offers, count = rc.offers.list(offset=offset, limit=limit, approved=True, active=True, launched=True, showcase=True)
	pages = paginate(page, count, per_page)
	return render_template('site/hm/catalog.html', offers=offers, pages=pages)

@bp.route('/catalog/old')
def catalog_old():
	return render_template('site/hm/catalog-old.html')
