# -*- coding: utf-8 -*-
from flask import render_template, g, request, abort, redirect, flash, url_for, jsonify, session
from heymoose import app
from heymoose.admin import blueprint as bp
from heymoose.core import actions as a
from heymoose.core.actions import roles
from heymoose.utils import convert, gen, times
from heymoose.utils.shortcuts import do_or_abort, paginate
from heymoose.views import common as cmnviews
from heymoose.forms import forms
from heymoose.db.models import Contact, GamakApp, UserInfo, OrderInfo
from heymoose.db.actions import invites
from heymoose.mail import marketing as mmail
from heymoose.mail import transactional as tmail
from datetime import datetime
import base64

SESSION_APPS_SHOW_DELETED = 'admin_apps_show_deleted'

@bp.route('/')
def index():
	return render_template('admin/index.html', params=g.params)

@bp.route('/viewmail')
def viewmail():
	filename = request.args.get('file', '')
	if filename:
		return render_template('mail/{0}.html'.format(filename))


@bp.route('/orders/')
def orders():
	page = convert.to_int(request.args.get('page'), 1)
	count = a.orders.get_orders_count()
	per_page = app.config.get('ADMIN_ORDERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	ods = a.orders.get_orders(offset=offset, limit=limit, full=True)
	return render_template('admin/orders.html', orders=ods, pages=pages)

@bp.route('/orders/stats')
def orders_stats():
	return render_template('admin/orders-stats.html')

@bp.route('/orders/settings', methods=['GET', 'POST'])
def orders_settings():
	banner_form = forms.BannerSizeForm()
	city_form = forms.CityForm()
	return render_template('admin/orders-settings.html',
		banner_form=banner_form, city_form=city_form)

@bp.route('/orders/<int:id>/', methods=['GET', 'POST'])
def orders_info(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	form = forms.OrderBlockForm(request.form)
	if request.method == 'POST' and form.validate():
		if not order.disabled:
			a.orders.disable_order(order.id)
			order_info = OrderInfo.query.get_or_create(order_id=order.id)
			order_info.block_reason = form.reason.data
			order_info.block_date = datetime.now()
			order_info.save()
			if form.mail.data: tmail.user_order_blocked(order, form.reason.data)
			tmail.admin_order_blocked(order, g.user, form.reason.data)
			flash(u'Заказ заблокиорван', 'success')
			return redirect(url_for('.orders_info', id=order.id))
		else:
			actn = request.form.get('action', 'unblock')
			if actn == 'unblock':
				a.orders.enable_order(order.id)
				if form.mail.data: tmail.user_order_unblocked(order)
				tmail.admin_order_unblocked(order, g.user)
				flash(u'Заказ разблокиорван', 'success')
			elif actn == 'notify':
				order_info = OrderInfo.query.get_or_create(order_id=order.id)
				order_info.block_reason = form.reason.data
				order_info.block_date = datetime.now()
				order_info.save()
				if form.mail.data: tmail.user_order_moderation_failed(order, form.reason.data)
				tmail.admin_order_moderation_failed(order, g.user, form.reason.data)
				flash(u'Пользователь уведомлен', 'success')
			return redirect(url_for('.orders_info', id=order.id))
	return render_template('admin/orders-info.html', order=order, form=form)

@bp.route('/orders/<int:id>/edit', methods=['GET', 'POST'])
def orders_info_edit(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	cities = [dict(id=city.id, name=city.name) for city in a.cities.get_cities()]
	order_cities = [dict(id=city.id, name=city.name) for city in order.cities] if order.cities else []
	
	form_args = dict(
		ordername = order.title,
		orderurl = order.url,
		orderbalance = order.account.balance,
		ordercpa = order.cpa,
		orderautoapprove = order.auto_approve,
		orderreentrant = order.reentrant,
		orderallownegativebalance = order.account.allow_negative_balance,
		ordermale = u'' if order.male is None else unicode(order.male),
		orderminage = order.min_age,
		ordermaxage = order.max_age,
		orderminhour = order.min_hour,
		ordermaxhour = order.max_hour,
		ordercitiesfilter = order.city_filter_type
	)
	
	if order.is_regular():
		form_args.update(orderdesc = order.description)
		cls = forms.AdminRegularOrderEditForm
	elif order.is_banner():
		cls = forms.AdminBannerOrderEditForm
	elif order.is_video():
		form_args.update(ordervideourl = order.video_url)
		cls = forms.AdminVideoOrderEditForm
		
	form = cls(request.form, **form_args)
		
	if request.method == 'POST' and form.validate():
		kwargs = dict()
		male = convert.to_bool(form.ordermale.data)
		
		if form.ordername.data != order.title: kwargs.update(title=form.ordername.data)
		if form.orderurl.data != order.url: kwargs.update(url=form.orderurl.data)
		if float(form.ordercpa.data) != order.cpa: kwargs.update(cpa=form.ordercpa.data)
		if form.orderallownegativebalance.data != order.account.allow_negative_balance: kwargs.update(allow_negative_balance=form.orderallownegativebalance.data)
		if form.orderautoapprove.data != order.auto_approve: kwargs.update(auto_approve=form.orderautoapprove.data)
		if form.orderreentrant.data != order.reentrant: kwargs.update(reentrant=form.orderreentrant.data)
		if male != order.male: kwargs.update(male=male)
		if form.orderminage.data != order.min_age: kwargs.update(min_age=form.orderminage.data)
		if form.ordermaxage.data != order.max_age: kwargs.update(max_age=form.ordermaxage.data)
		if form.orderminhour.data != order.min_hour: kwargs.update(min_hour=form.orderminhour.data)
		if form.ordermaxhour.data != order.max_hour: kwargs.update(max_hour=form.ordermaxhour.data)
		
		old_cities = frozenset([city.id for city in order.cities])
		new_cities = frozenset([int(x) for x in form.ordercities.data.split(',')] if form.ordercities.data else [])
		if new_cities != old_cities: kwargs.update(city=list(new_cities))
		
		city_filter_type = (form.ordercitiesfilter.data or None) if new_cities else None
		if city_filter_type != order.city_filter_type: kwargs.update(city_filter_type=city_filter_type)
				
		if order.is_regular():
			if form.orderdesc.data != order.description: kwargs.update(description=form.orderdesc.data)
			if form.orderimage.data is not None: kwargs.update(image=base64.encodestring(request.files['orderimage'].stream.read()))
		elif order.is_banner():
			pass
		elif order.is_video():
			if form.ordervideourl.data != order.video_url: kwargs.update(video_url=form.ordervideourl.data)
		
		if kwargs.keys():
			a.orders.update_order(order.id, **kwargs)
			flash(u'Заказ успешно обновлен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.orders_info', id=order.id))
		
	return render_template('admin/orders-info-edit.html', order=order, form=form,
		cities=cities, order_cities=order_cities)

@bp.route('/orders/<int:id>/banners')
def orders_info_banners(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	if not order.is_banner(): abort(404)
	return render_template('admin/orders-info-banners.html', order=order)

@bp.route('/orders/<int:id>/apps', methods=['GET', 'POST'])
def orders_info_apps(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	aps = do_or_abort(a.apps.get_apps, offset=0, limit=10000, full=True)
	form = forms.OrderAppsForm(request.form, filter=order.app_filter_type)
	if request.method == 'POST' and form.validate():
		a.orders.update_order(order.id,
			app_filter_type=form.filter.data,
			app=[int(x) for x in form.apps.data.split(',')] if form.apps.data else []
		)
		flash(u'Таргетинг успешно обновлен', 'success')
		return redirect(url_for('.orders_info_apps', id=order.id))
	return render_template('admin/orders-info-apps.html', order=order, apps=aps, form=form)

@bp.route('/orders/<int:id>/actions')
def orders_info_actions(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	page = convert.to_int(request.args.get('page'), 1)
	count = a.actions.get_actions_count(offerId=order.offer_id)
	per_page = app.config.get('ADMIN_ACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	acts = do_or_abort(a.actions.get_actions, 
		offset=offset, limit=limit, full=True, offerId=order.offer_id)
	return render_template('admin/orders-info-actions.html', order=order, actions=acts, pages=pages)

@bp.route('/orders/<int:id>/audience')
def orders_info_audience(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return render_template('admin/orders-info-audience.html', order=order)

@bp.route('/orders/<int:id>/stats')
def orders_info_stats(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return render_template('admin/orders-info-stats.html', order=order)


@bp.route('/apps/', methods=['GET', 'POST'])
def apps():
	page = convert.to_int(request.args.get('page'), 1)
	form = forms.AppsShowDeletedForm(request.form, show=session.get(SESSION_APPS_SHOW_DELETED, False))
	if request.method == 'POST' and form.validate():
		session[SESSION_APPS_SHOW_DELETED] = form.show.data
		page = 1
	
	count = a.apps.get_apps_count(form.show.data)
	per_page = app.config.get('ADMIN_APPS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	aps = do_or_abort(a.apps.get_apps, with_deleted=form.show.data,
					offset=offset, limit=limit, full=True)
	return render_template('admin/apps.html', apps=aps, pages=pages, form=form)

@bp.route('/apps/traffic')
def apps_traffic():
	sets = a.settings.get_settings()
	form = forms.TrafficAnalyzeForm(request.args, cpc=sets.c_min_safe())
	aps = list()
	summary = dict(dau_day0=0, dau_day1=0, dau_day2=0, dau_day3=0, dau_day4=0,
		dau_day5=0, dau_day6=0, dau_average=0.0)
	if form.validate():
		max_d = float(form.cpc.data) - sets.m
		aps = a.apps.get_apps(max_d=max_d, limit=9999, full=True)
		for app in aps:
			if not app.stats: continue
			summary['dau_average'] += app.stats.dau_average or 0.0
			for i in range(7):
				attr = 'dau_day{0}'.format(i)
				summary[attr] += getattr(app.stats, attr) or 0
	return render_template('admin/apps-traffic.html', form=form, apps=aps, summary=summary)

@bp.route('/apps/stats')
def apps_stats():
	return render_template('admin/apps-stats.html')

@bp.route('/apps/<int:id>')
def apps_info(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return render_template('admin/apps-info.html', app=app)

@bp.route('/apps/<int:id>/edit', methods=['GET', 'POST'])
def apps_info_edit(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	form = forms.AdminAppEditForm(request.form, apptitle=app.title, appurl=app.url, 
		appplatform=app.platform, appdeleted=app.deleted, appd=app.d, appt=app.t)
	if request.method == 'POST' and form.validate():
		kwargs = dict()
		if form.apptitle.data != app.title: kwargs.update(title=form.apptitle.data)
		if form.appurl.data != app.url: kwargs.update(url=form.appurl.data, callback=form.appurl.data)
		if form.appplatform.data != app.platform: kwargs.update(platform=form.appplatform.data)
		if float(form.appd.data) != app.d: kwargs.update(d=form.appd.data)
		if float(form.appt.data) != app.t: kwargs.update(t=form.appt.data)
		if form.appdeleted.data != app.deleted: kwargs.update(deleted=form.appdeleted.data)
		
		if kwargs.keys():
			a.apps.update_app(app.id, **kwargs)
			flash(u'Приложение успешно обновлено', u'success')
		else:
			flash(u'Вы не изменили ни одного поля', u'warning')
		return redirect(url_for('.apps_info', id=app.id))
	
	return render_template('admin/apps-info-edit.html', app=app, form=form)

@bp.route('/apps/<int:id>/actions')
def apps_info_actions(id):
	ap = do_or_abort(a.apps.get_app, id, full=True)
	page = convert.to_int(request.args.get('page'), 1)
	count = a.actions.get_actions_count(appId=ap.id)
	per_page = app.config.get('ADMIN_ACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	acts = do_or_abort(a.actions.get_actions, offset=offset, limit=limit, full=True, appId=ap.id)
	return render_template('admin/apps-info-actions.html', app=ap, actions=acts, pages=pages)

@bp.route('/apps/<int:id>/audience')
def apps_info_audience(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return render_template('admin/apps-info-audience.html', app=app)

@bp.route('/apps/<int:id>/stats')
def apps_info_stats(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return render_template('admin/apps-info-stats.html', app=app)


@bp.route('/actions/')
def actions():
	page = convert.to_int(request.args.get('page'), 1)
	count = a.actions.get_actions_count()
	per_page = app.config.get('ADMIN_ACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	acts = do_or_abort(a.actions.get_actions, offset=offset, limit=limit, full=True)
	return render_template('admin/actions.html', actions=acts, pages=pages)

@bp.route('/actions/stats')
def actions_stats():
	return render_template('admin/actions-stats.html')

@bp.route('/actions/<int:id>')
def actions_info(id):
	action = do_or_abort(a.actions.get_action, id, full=True)
	return render_template('admin/actions-info.html', action=action)

@bp.route('/actions/<int:id>/stats')
def actions_info_stats(id):
	action = do_or_abort(a.actions.get_action, id, full=True)
	return render_template('admin/actions-info-stats.html', action=action)


@bp.route('/users/')
def users():
	page = convert.to_int(request.args.get('page'), 1)
	count = a.users.get_users_count()
	per_page = app.config.get('ADMIN_USERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	usrs = do_or_abort(a.users.get_users, offset=offset, limit=limit, full=True)
	return render_template('admin/users.html', users=usrs, pages=pages)

@bp.route('/users/customers/')
def users_customers():
	role = 'CUSTOMER'
	page = convert.to_int(request.args.get('page'), 1)
	count = a.users.get_users_count(role=role)
	per_page = app.config.get('ADMIN_USERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	usrs = do_or_abort(a.users.get_users, role=role, offset=offset, limit=limit, full=True)
	return render_template('admin/users-customers.html', customers=usrs, pages=pages)

@bp.route('/users/developers/')
def users_developers():
	role = 'DEVELOPER'
	page = convert.to_int(request.args.get('page'), 1)
	count = a.users.get_users_count(role=role)
	per_page = app.config.get('ADMIN_USERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	usrs = do_or_abort(a.users.get_users, role=role, offset=offset, limit=limit, full=True)
	return render_template('admin/users-developers.html', developers=usrs, pages=pages)

@bp.route('/users/invites')
def users_invites():
	return render_template('admin/users-invites.html')

@bp.route('/users/register/customer', methods=['GET', 'POST'])
def users_register_customer():
	form = forms.CustomerRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(a.users.add_user,
			email=form.email.data,
			password_hash=gen.generate_password_hash(form.password.data),
			first_name=form.first_name.data,
			last_name=form.last_name.data,
			organization=form.organization.data,
			phone=form.phone.data,
			messenger_type=form.messenger_type.data,
			messenger_uid=form.messenger_uid.data)
		user = do_or_abort(a.users.get_user_by_email, form.email.data, full=True)
		if user:
			a.users.confirm_user(user.id)
			a.users.add_user_role(user.id, roles.CUSTOMER)
			user.roles.append(roles.CUSTOMER)
			flash(u'Рекламодатель успешно зарегистрирован', 'success')
			mmail.lists_add_user(user)
			return redirect(url_for('.users_info', id=user.id))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
	
	return render_template('admin/users-register-customer.html', form=form)

@bp.route('/users/stats')
def users_stats():
	return render_template('admin/users-stats.html')

@bp.route('/users/<int:id>', methods=['GET', 'POST'])
def users_info(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	form = forms.UserBlockForm(request.form)
	if request.method == 'POST':
		if not user.blocked and form.validate():
			a.users.block_user(user.id)
			user_info = UserInfo.query.get_or_create(user_id=user.id)
			user_info.block_reason = form.reason.data
			user_info.block_date = datetime.now()
			user_info.save()
			if form.mail.data:
				tmail.user_blocked(user, form.reason.data)
			tmail.admin_user_blocked(user, g.user, form.reason.data)
			flash(u'Учетная запись заблокирована', 'success')
			return redirect(url_for('.users_info', id=user.id))
		elif user.blocked:
			a.users.unblock_user(user.id)
			flash(u'Учетная запись разблокирована', 'success')
			return redirect(url_for('.users_info', id=user.id))
	
	return render_template('admin/users-info.html', user=user, form=form)

@bp.route('/users/<int:id>/stats')
def users_info_stats(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	return render_template('admin/users-info-stats.html', user=user)

@bp.route('/users/<int:id>/orders')
def users_info_orders(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	if not user.is_customer(): abort(404)
	
	page = convert.to_int(request.args.get('page'), 1)
	count = a.orders.get_orders_count(user_id=user.id)
	per_page = app.config.get('ADMIN_ORDERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	ods = a.orders.get_orders(user_id=user.id, offset=offset, limit=limit, full=True)
	return render_template('admin/users-info-orders.html', user=user, orders=ods, pages=pages)

@bp.route('/users/<int:id>/apps')
def users_info_apps(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	if not user.is_developer(): abort(404)
	
	page = convert.to_int(request.args.get('page'), 1)
	count = a.apps.get_apps_count(user_id=user.id)
	per_page = app.config.get('ADMIN_APPS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	with_deleted = session.get(SESSION_APPS_SHOW_DELETED, False)
	aps = do_or_abort(a.apps.get_apps, with_deleted=with_deleted,
					user_id=user.id, offset=offset, limit=limit, full=True)
	return render_template('admin/users-info-apps.html', user=user, apps=aps, pages=pages)

@bp.route('/users/<int:id>/edit', methods=['GET', 'POST'])
def users_info_edit(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	form_args = dict(
		first_name = user.first_name,
		last_name = user.last_name,
		phone = user.phone,
		organization = user.organization,
		messenger_type = user.messenger_type,
		messenger_uid = user.messenger_uid,
		email = user.email,
		confirmed = user.confirmed
	)
	if user.is_customer():
		form = forms.AdminCustomerEditForm(request.form, **form_args)
	else:
		form = forms.AdminDeveloperEditForm(request.form, **form_args)
	form.user = user
	
	if request.method == 'POST' and form.validate():
		upd_args = dict()
		if form.first_name.data != user.first_name: upd_args.update(first_name=form.first_name.data)
		if form.last_name.data != user.last_name: upd_args.update(last_name=form.last_name.data)
		if form.organization.data != user.organization: upd_args.update(organization=form.organization.data)
		if form.phone.data != user.phone: upd_args.update(phone=form.phone.data)
		if form.messenger_type.data != user.messenger_type or form.messenger_uid.data != user.messenger_uid:
			upd_args.update(messenger_type=form.messenger_type.data, messenger_uid=form.messenger_uid.data)
		if form.email.data != user.email: upd_args.update(email=form.email.data)
		if form.confirmed.data != user.confirmed: upd_args.update(confirmed=form.confirmed.data)
		if upd_args.keys():
			a.users.update_user(user.id, **upd_args)
			flash(u'Профиль успешно изменен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.users_info', id=user.id))
	
	return render_template('admin/users-info-edit.html', user=user, form=form)

@bp.route('/users/<int:id>/password', methods=['GET', 'POST'])
def users_info_password_change(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	form = forms.AdminPasswordChangeForm(request.form)
	if request.method == 'POST' and form.validate():
		a.users.update_user(user.id, password_hash=gen.generate_password_hash(form.password.data))
		flash(u'Пароль пользователя успешно изменен', 'success')
		return redirect(url_for('.users_info', id=user.id))
	return render_template('admin/users-info-password-change.html', user=user, form=form)

@bp.route('/users/<int:id>/a/lists/add')
def users_info_lists_add(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	if mmail.lists_add_user(user, mail_if_failed=False):
		flash(u'Пользователь добавлен в списки рассылки', 'success')
	else:
		flash(u'Ошибка при добавлении пользователя в списки рассылки', 'error')
	return redirect(url_for('.users_info', id=user.id))

@bp.route('/users/<int:id>/balance', methods=['GET', 'POST'])
def users_info_balance(id):
	user = do_or_abort(a.users.get_user_by_id, id)
	delete_form = forms.WithdrawalDeleteForm()
	withdrawals = None
	if user.is_customer():
		account = user.customer_account
		form = forms.BalanceForm(request.form)
		if request.method == 'POST' and form.validate():
			a.users.increase_customer_balance(user.id, round(form.amount.data, 2))
			flash(u'Баланс успешно пополнен', 'success')
			return redirect(url_for('.users_info_balance', id=user.id))
	elif user.is_developer():
		account = user.developer_account
		form = forms.BalanceForm(request.form, amount=account.balance)
		if request.method == 'POST' and form.validate():
			a.users.make_user_withdrawal(user.id, round(form.amount.data, 2))
			flash(u'Выплата разработчику успешно создана', 'success')
			return redirect(url_for('.users_info_balance', id=user.id))
		
		withdrawals = a.users.get_user_withdrawals(user.id)
	else:
		flash(u'Пользователь не имеет счета', 'error')
		return redirect(url_for('.users_info', id=user.id))
	
	page = convert.to_int(request.args.get('page'), 1)
	count = a.accounts.get_account_transactions_count(account.id)
	per_page = app.config.get('ADMIN_TRANSACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	transactions = a.accounts.get_account_transactions(account_id=account.id, offset=offset, limit=limit)
	return render_template('admin/users-info-balance.html', transactions=transactions,
		withdrawals=withdrawals, pages=pages, user=user, form=form, delete_form=delete_form)
	
@bp.route('/users/<int:id>/balance/withdrawals/<int:wid>/approve', methods=['POST'])
def users_info_approve_withdrawal(id, wid):
	user = do_or_abort(a.users.get_user_by_id, id)
	a.users.approve_user_withdrawal(user.id, wid)
	flash(u'Выплата разработчику подтверждена', 'success')
	return redirect(url_for('.users_info_balance', id=user.id))

@bp.route('/users/<int:id>/balance/withdrawals/<int:wid>/delete', methods=['POST'])
def users_info_delete_withdrawal(id, wid):
	user = do_or_abort(a.users.get_user_by_id, id)
	form = forms.WithdrawalDeleteForm(request.form)
	if form.validate():
		a.users.delete_user_withdrawal(user.id, wid, form.reason.data)
		flash(u'Выплата разработчику отменена', 'success')
	else:
		flash(u'При выплате разработчику произошла ошибка', 'error')
	return redirect(url_for('.users_info_balance', id=user.id))


@bp.route('/performers/')
def performers():
	page = convert.to_int(request.args.get('page'), 1)
	count = a.performers.get_performers_count()
	per_page = app.config.get('ADMIN_PERFORMERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	perfs = do_or_abort(a.performers.get_performers, offset=offset, limit=limit, full=True)
	return render_template('admin/performers.html', performers=perfs, pages=pages)

@bp.route('/performers/stats')
def performers_stats():
	return render_template('admin/performers-stats.html')

@bp.route('/performers/<int:id>')
def performers_info(id):
	performer = do_or_abort(a.performers.get_performer, id, full=True)
	return render_template('admin/performers-info.html', performer=performer)

@bp.route('/performers/<int:id>/actions')
def performers_info_actions(id):
	performer = do_or_abort(a.performers.get_performer, id, full=True)
	page = convert.to_int(request.args.get('page'), 1)
	count = a.actions.get_actions_count(performerId=performer.id)
	per_page = app.config.get('ADMIN_ACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	acts = do_or_abort(a.actions.get_actions, 
		offset=offset, limit=limit, full=True, performerId=performer.id)
	return render_template('admin/performers-info-actions.html', performer=performer, actions=acts, pages=pages)

@bp.route('/performers/<int:id>/stats')
def performers_info_stats(id):
	performer = do_or_abort(a.performers.get_performer, id, full=True)
	return render_template('admin/performers-info-stats.html', performer=performer)


@bp.route('/settings/', methods=['GET', 'POST'])
def settings():
	sets = a.settings.get_settings()
	form = forms.SettingsForm(request.form, obj=sets)
	if request.method == 'POST' and form.validate():
		args = dict()
		if float(form.c_min.data) != sets.c_min: args.update(c_min=form.c_min.data)
		if float(form.m.data) != sets.m: args.update(m=form.m.data)
		if float(form.q.data) != sets.q: args.update(q=form.q.data)
		if args.keys():
			a.settings.update_settings(**args)
			if form.mail.data and 'c_min' in args.keys():
				tmail.user_order_priced_off(a.orders.get_price_off_orders(), form.c_min.data)
			flash(u'Параметры успешно изменены', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.settings'))
	return render_template('admin/settings.html', settings=sets, form=form)


@bp.route('/feedback/', methods=['GET', 'POST'])
def feedback():
	filters = {
		'contacts': (~(Contact.partner == True), ),
		'partners': (Contact.partner == True, )
	}.get(request.args.get('filter', ''), (()) )
	
	if request.method == 'POST':
		contacts = Contact.query.filter(Contact.read == False, *filters)
		for contact in contacts: # For some reason set/execute query not working
			contact.read = True
			contact.save()
		g.feedback_unread = Contact.query.filter(Contact.read == False).count()
	
	page = convert.to_int(request.args.get('page'), 1)
	count = Contact.query.filter(*filters).count()
	per_page = app.config.get('ADMIN_CONTACTS_PER_PAGE', 10)
	offset, limit, pages = paginate(page, count, per_page)
	contacts = Contact.query.filter(*filters).descending(Contact.date).skip(offset).limit(limit)
	return render_template('admin/feedback.html', contacts=contacts.all(), pages=pages)


@bp.route('/orders/<int:id>/q/enable', methods=['POST'])
def ajax_orders_enable(id):
	do_or_abort(a.orders.enable_order, id)
	return 'OK'

@bp.route('/orders/<int:id>/q/disable', methods=['POST'])
def ajax_orders_disable(id):
	do_or_abort(a.orders.disable_order, id)
	return 'OK'

@bp.route('/orders/q/banner-sizes')
def ajax_orders_get_banner_sizes():
	sizes = sorted(a.bannersizes.get_banner_sizes(False), key=lambda s: s.width)
	data = [dict(id=s.id, width=s.width, height=s.height, disabled=s.disabled) for s in sizes]
	return jsonify(values=data)

@bp.route('/orders/q/banner-sizes/new', methods=['POST'])
def ajax_orders_add_banner_size():
	form = forms.BannerSizeForm(request.form)
	if form.validate():
		id = a.bannersizes.add_banner_size(form.width.data, form.height.data)
		return unicode(id)
	return u'Размер введен неверно', 400

@bp.route('/order/q/banner-sizes/enable', methods=['POST'])
def ajax_orders_enable_banner_size():
	id = int(request.form.get('id', '0'))
	value = int(request.form.get('value', '0'))
	print id, value
	a.bannersizes.set_banner_size_enabled(id, bool(value))
	return 'OK'

@bp.route('/orders/q/cities')
def ajax_orders_get_cities():
	cities = sorted(a.cities.get_cities(False), key=lambda x: x.name)
	data = [dict(id=c.id, name=c.name, disabled=c.disabled) for c in cities]
	return jsonify(values=data)

@bp.route('/orders/q/cities/add', methods=['POST'])
def ajax_orders_add_city():
	form = forms.CityForm(request.form)
	if form.validate():
		id = a.cities.add_city(form.name.data)
		return unicode(id)
	return u'Название введено неверно', 400

@bp.route('/orders/q/cities/update', methods=['POST'])
def ajax_orders_update_city():
	form = forms.CityForm(request.form)
	if form.validate():
		id = int(form.id.data) if form.id.data else 0
		a.cities.update_city(id, form.name.data)
		return 'OK'
	return u'Название введено неверно', 400

@bp.route('/order/q/cities/enable', methods=['POST'])
def ajax_orders_enable_city():
	id = int(request.form.get('id', '0'))
	value = int(request.form.get('value', '0'))
	a.cities.update_city(id, disabled=not bool(value))
	return 'OK'


@bp.route('/apps/q/ctr')
def ajax_apps_ctr():
	'''ids = request.args.getlist('id', int)
	stats = a.stats.get_stats_ctr_by_ids(app_ids=ids, fm=times.delta(datetime.now(), days=-3))
	result = dict([(s.id, dict(actions=s.actions, shows=s.shows, ctr='%.4f' % s.ctr)) for s in stats])
	return jsonify(result)'''
	return jsonify(disabled=1)

@bp.route('/orders/q/ctr')
def ajax_orders_ctr():
	'''ids = request.args.getlist('id', int)
	stats = a.stats.get_stats_ctr_by_ids(offer_ids=ids, fm=times.delta(datetime.now(), days=-3))
	result = dict([(s.id, dict(actions=s.actions, shows=s.shows, ctr='%.4f' % s.ctr)) for s in stats])
	return jsonify(result)'''
	return jsonify(disabled=1)

@bp.route('/orders/<int:id>/q/audience/')
def ajax_orders_info_audience(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return cmnviews.json_get_audience(offer_id=order.offer_id)

@bp.route('/apps/<int:id>/q/audience/')
def ajax_apps_info_audience(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return cmnviews.json_get_audience(app_id=app.id)


@bp.route('/orders/<int:id>/stats/q/ctr/')
def ajax_orders_info_stats_ctr(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return cmnviews.json_get_ctr(offer_id=order.offer_id)

@bp.route('/apps/<int:id>/stats/q/ctr/')
def ajax_apps_info_stats_ctr(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return cmnviews.json_get_ctr(app_id=app.id)

@bp.route('/users/invites/q/get/')
def ajax_get_invite():
	return invites.create_invite()

@bp.route('/actions/<int:id>/q/approve', methods=['POST'])
def ajax_action_approve(id):
	do_or_abort(a.actions.approve_action, id)
	return 'OK'

@bp.route('/actions/<int:id>/q/delete', methods=['POST'])
def ajax_action_delete(id):
	do_or_abort(a.actions.delete_action, id)
	return 'OK'
	

@bp.route('/gamak/apps/')
def gamak_apps():
	aps = GamakApp.query.descending(GamakApp.date).all()
	return render_template('admin/gamak-apps.html', apps=aps)

@bp.route('/gamak/apps/new', methods=['GET', 'POST'])
def gamak_apps_new():
	form = forms.GamakAppForm(request.form)
	if request.method == 'POST' and form.validate():
		app = GamakApp(date=datetime.now(), mime_type=form.image.mime_type)
		form.populate_obj(app)
		app.save()
		request.files['image'].save(app.image_path())
		flash(u'Приложение успешно добавлено', 'success')
		return redirect(url_for('.gamak_apps'))
	return render_template('admin/gamak-apps-edit.html', form=form)

@bp.route('/gamak/apps/<id>', methods=['GET', 'POST'])
def gamak_apps_edit(id):
	app = GamakApp.query.get_or_404(id)
	form = forms.GamakAppEditForm(request.form, obj=app)
	if request.method == 'POST' and form.validate():
		form.populate_obj(app)
		print form.image.data
		if form.image.data:
			app.mime_type = form.image.mime_type
			request.files['image'].save(app.image_path())
		app.save()
		flash(u'Приложение успешно изменено', 'success')
		return redirect(url_for('.gamak_apps'))
	return render_template('admin/gamak-apps-edit.html', form=form, app=app)

