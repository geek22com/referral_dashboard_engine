# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash, jsonify
from heymoose import app
from heymoose.cabinet import blueprint as bp
from heymoose.forms import forms
from heymoose.core import actions
from heymoose.core.data import OrderTypes
from heymoose.utils import convert, robokassa, times
from heymoose.utils.shortcuts import do_or_abort, paginate
from heymoose.utils.gen import generate_password_hash
from heymoose.views.common import json_get_ctr
from decorators import customer_only, developer_only
from datetime import datetime
import base64, os


@bp.route('/')
def index():
	if g.user.is_admin():
		return redirect(url_for('admin.index'))
	elif g.user.is_developer():
		return redirect(url_for('.apps'))
	elif g.user.is_customer():
		return redirect(url_for('.orders'))
	else:
		app.logger().error("Shit happened: user has unknown role in user cabinet")
		abort(403)


@bp.route('/orders/')
@customer_only
def orders():
	page = convert.to_int(request.args.get('page'), 1)
	count = actions.orders.get_orders_count(user_id=g.user.id)
	per_page = app.config.get('ADMIN_ORDERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	ods = actions.orders.get_orders(user_id=g.user.id, offset=offset, limit=limit, full=True)
	return render_template('cabinet/orders.html', orders=ods, pages=pages)

@bp.route('/orders/new', methods=['GET', 'POST'])
@customer_only
def orders_new():
	sizes = actions.bannersizes.get_banner_sizes()
	choices = [(s.id, '{0} x {1}'.format(s.width, s.height)) for s in sizes]
	cities = [dict(id=city.id, name=city.name) for city in actions.cities.get_cities()]
	
	form = forms.BannerOrderForm(request.form)
	form.orderbannersize.choices = choices
	if request.method == 'POST' and form.validate():
		id = do_or_abort(actions.orders.add_banner_order,
			user_id=g.user.id,
			title=form.ordername.data,
			url=form.orderurl.data,
			balance=form.orderbalance.data,
			cpa=form.ordercpa.data,
			allow_negative_balance=False,
			auto_approve=True,
			reentrant=True,
			male=form.ordermale.data,
			min_age=form.orderminage.data,
			max_age=form.ordermaxage.data,
			min_hour=form.orderminhour.data,
			max_hour=form.ordermaxhour.data,
			city_filter_type=form.ordercitiesfilter.data,
			city=[int(x) for x in form.ordercities.data.split(',')] if form.ordercities.data else [],
			banner_size=form.orderbannersize.data,
			banner_mime_type=form.orderimage.mime_type,
			image=base64.encodestring(request.files['orderimage'].stream.read()))
		flash(u'Заказ успешно создан.', 'success')
		return redirect(url_for('.orders_info', id=id))
	return render_template('cabinet/orders-new.html', form=form, cities=cities)
	
@bp.route('/orders/<int:id>/')
@customer_only
def orders_info(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	return render_template('cabinet/orders-info.html', order=order)

@bp.route('/orders/<int:id>/banners', methods=['GET', 'POST'])
@customer_only
def orders_info_banners(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id or not order.is_banner(): abort(404)
	
	order_sizes = [banner.size.id for banner in order.banners]
	all_sizes = actions.bannersizes.get_banner_sizes()
	size_choices = [(s.id, '{0} x {1}'.format(s.width, s.height)) for s in all_sizes if s.id not in order_sizes]
	
	if size_choices:
		form = forms.BannerForm(request.form)
		form.size.choices = size_choices
		if request.method == 'POST' and form.validate():
			actions.orders.add_order_banner(order.id, form.size.data, form.image.mime_type,
				base64.encodestring(request.files['image'].stream.read()))
			flash(u'Баннер успешно загружен', 'success')
			return redirect(url_for('.orders_info_banners', id=order.id))
	else:
		form = None
	
	return render_template('cabinet/orders-info-banners.html', order=order, form=form)

@bp.route('/orders/<int:id>/banners/<int:bid>/delete', methods = ['POST'])
@customer_only
def orders_info_banners_delete(id, bid):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id or not order.is_banner(): abort(404)
	if bid not in [banner.id for banner in order.banners]: abort(404)
	if len(order.banners) <= 1: abort(403)
	
	actions.orders.delete_order_banner(id, bid)
	flash(u'Баннер удален', 'success')
	return redirect(url_for('.orders_info_banners', id=order.id))

@bp.route('/orders/<int:id>/edit', methods=['GET', 'POST'])
@customer_only
def orders_info_edit(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	cities = [dict(id=city.id, name=city.name) for city in actions.cities.get_cities()]
	order_cities = [dict(id=city.id, name=city.name) for city in order.cities] if order.cities else []
	
	form_args = dict(
		ordername = order.title,
		orderurl = order.url,
		orderbalance = order.account.balance,
		ordercpa = order.cpa,
		ordermale = u'' if order.male is None else unicode(order.male),
		orderminage = order.min_age,
		ordermaxage = order.max_age,
		orderminhour = order.min_hour,
		ordermaxhour = order.max_hour,
		ordercitiesfilter = order.city_filter_type
	)
	
	if order.is_regular():
		form_args.update(orderdesc = order.description)
		cls = forms.RegularOrderEditForm
	elif order.is_banner():
		cls = forms.BannerOrderEditForm
	elif order.is_video():
		form_args.update(ordervideourl = order.video_url)
		cls = forms.VideoOrderEditForm
		
	form = cls(request.form, **form_args)
		
	if request.method == 'POST' and form.validate():
		kwargs = dict()
		male = convert.to_bool(form.ordermale.data)
		city_filter_type = form.ordercitiesfilter.data if form.ordercitiesfilter.data else None
		
		if form.ordername.data != order.title: kwargs.update(title=form.ordername.data)
		# if form.orderurl.data != order.url: kwargs.update(url=form.orderurl.data)
		if form.ordercpa.data != order.cpa: kwargs.update(cpa=form.ordercpa.data)
		if male != order.male: kwargs.update(male=male)
		if form.orderminage.data != order.min_age: kwargs.update(min_age=form.orderminage.data)
		if form.ordermaxage.data != order.max_age: kwargs.update(max_age=form.ordermaxage.data)
		if form.orderminhour.data != order.min_hour: kwargs.update(min_hour=form.orderminhour.data)
		if form.ordermaxhour.data != order.max_hour: kwargs.update(max_hour=form.ordermaxhour.data)
		if city_filter_type != order.city_filter_type: kwargs.update(city_filter_type=city_filter_type)
		
		old_cities = frozenset([city.id for city in order.cities])
		new_cities = frozenset([int(x) for x in form.ordercities.data.split(',')] if form.ordercities.data else [])
		if new_cities != old_cities: kwargs.update(city=list(new_cities))
				
		if order.is_regular():
			if form.orderdesc.data != order.description: kwargs.update(description=form.orderdesc.data)
			if form.orderimage.data is not None: kwargs.update(image=base64.encodestring(request.files['orderimage'].stream.read()))
		elif order.is_banner():
			pass
		elif order.is_video():
			if form.ordervideourl.data != order.video_url: kwargs.update(video_url=form.ordervideourl.data)
		
		if kwargs.keys():
			actions.orders.update_order(order.id, **kwargs)
			flash(u'Заказ успешно обновлен', 'success')
		else:
			flash(u'Вы не изменили ни одного поля', 'warning')
		return redirect(url_for('.orders_info', id=order.id))
		
	return render_template('cabinet/orders-info-edit.html', order=order, form=form,
		cities=cities, order_cities=order_cities)
	
@bp.route('/orders/<int:id>/balance', methods=['GET', 'POST'])
@customer_only
def orders_info_balance(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	other_orders = [ord for ord in actions.orders.get_orders(user_id=g.user.id) if ord.id != order.id]
	order_choices = [(ord.account.id, ord.title) for ord in other_orders]
	
	form_in = forms.BalanceForm()
	form_out = forms.BalanceForm()
	form_transfer = forms.OrderBalanceTransferForm()
	form_transfer.order.choices = order_choices
	
	if request.method == 'POST':
		type = request.form.get('type', 'in')
		if type == 'in':
			form_in = forms.BalanceForm(request.form)
			if form_in.validate():
				actions.accounts.transfer(g.user.customer_account.id, order.account.id, form_in.amount.data)
				flash(u'Счет заказа успешно пополнен', 'success')
				return redirect(url_for('.orders_info', id=order.id))
		elif type == 'out':
			form_out = forms.BalanceForm(request.form)
			if form_out.validate():
				actions.accounts.transfer(order.account.id, g.user.customer_account.id, form_out.amount.data)
				flash(u'Средства успешно выведены со счета заказа', 'success')
				return redirect(url_for('.orders_info', id=order.id))
		elif type == 'transfer':
			form_transfer = forms.OrderBalanceTransferForm(request.form)
			form_transfer.order.choices = order_choices
			if form_transfer.validate():
				actions.accounts.transfer(order.account.id, form_transfer.order.data, form_transfer.amount.data)
				flash(u'Средства успешно переведены', 'success')
				return redirect(url_for('.orders_info', id=order.id))
		else:
			flash(u'Ошибка операции со счетом', 'error')
			return redirect(url_for('.orders_info', id=order.id))
	
	return render_template('cabinet/orders-info-balance.html', order=order,
			form_in=form_in, form_out=form_out, form_transfer=form_transfer)

@bp.route('/orders/<int:id>/stats')
@customer_only
def orders_info_stats(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	return render_template('cabinet/orders-info-stats.html', order=order)
	

@bp.route('/apps/')
@developer_only
def apps():
	page = convert.to_int(request.args.get('page'), 1)
	count = actions.apps.get_apps_count(user_id=g.user.id)
	per_page = app.config.get('ADMIN_APPS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	aps = do_or_abort(actions.apps.get_apps, user_id=g.user.id,
					offset=offset, limit=limit, full=True)
	return render_template('cabinet/apps.html', apps=aps, pages=pages)

@bp.route('/apps/new', methods=['GET', 'POST'])
@developer_only
def apps_new():
	form = forms.AppForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.apps.add_app,
			title=form.apptitle.data,
			user_id=g.user.id,
			callback=form.appurl.data,
			url=form.appurl.data,
			platform=form.appplatform.data)
		flash(u'Приложение успешно добавлено', 'success')
		return redirect(url_for('.apps'))
	return render_template('cabinet/apps-new.html', form=form)

@bp.route('/apps/<int:id>/')
@developer_only
def apps_info(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return render_template('cabinet/apps-info.html', app=app)

@bp.route('/apps/<int:id>/stats')
@developer_only
def apps_info_stats(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return render_template('cabinet/apps-info-stats.html', app=app)


@bp.route('/info')
def info():
	return render_template('cabinet/info.html')

@bp.route('/info/password', methods=['GET', 'POST'])
def info_password_change():
	form = forms.PasswordChangeForm(request.form)
	form.oldpassword.user = g.user
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.users.update_user, g.user.id,
			generate_password_hash(form.password.data))
		flash(u'Пароль успешно изменен', 'success')
		return redirect(url_for('.info'))
	return render_template('cabinet/info-password-change.html', form=form)

@bp.route('/info/balance', methods=['GET', 'POST'])
@customer_only
def info_balance():
	form = forms.BalanceForm(request.form)
	if request.method == 'POST' and form.validate():
		sum = form.amount.data
		url = robokassa.account_pay_url(
			account_id=g.user.customer_account.id,
			sum=round(sum, 2),
			email=g.user.email)
		return redirect(url)
	
	page = convert.to_int(request.args.get('page'), 1)
	_unused, count = actions.accounts.get_account_transactions(g.user.customer_account.id, 0, 1)
	per_page = app.config.get('ADMIN_TRANSACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	transactions, count = do_or_abort(actions.accounts.get_account_transactions,
							account_id=g.user.customer_account.id,
							offset=offset, limit=limit)
	return render_template('cabinet/info-balance.html', transactions=transactions,
						pages=pages, form=form)
	
@bp.route('/info/balance/success', methods=['POST'])
@customer_only
def info_balance_success():
	sum = request.form.get('OutSum', None)
	if sum is None: abort(400)
	return render_template('cabinet/info-balance-success.html', sum=float(sum))

@bp.route('/info/balance/fail', methods=['POST'])
@customer_only
def info_balance_fail():
	sum = request.form.get('OutSum', None)
	if sum is None: abort(400)
	return render_template('cabinet/info-balance-fail.html', sum=float(sum))
	

# @bp.route('/roles/new/customer')
def become_customer():
	'''Deprecated: customers are registered in admin blueprint'''
	if not g.user.is_customer():
		do_or_abort(actions.users.become_customer, g.user.id)
		flash(u'Поздравляем, теперь вы рекламодатель!', 'success')
	else:
		flash(u'Вы уже являетесь рекламодателем', 'error')
	return redirect(url_for('.orders'))

# @bp.route('/roles/new/developer')
def become_developer():
	'''Deprecated: developers register with invites'''
	if not g.user.is_developer():
		do_or_abort(actions.users.become_developer, g.user.id)
		flash(u'Поздравляем, теперь вы разработчик!', 'success')
	else:
		flash(u'Вы уже являетесь разработчиком', 'error')
	return redirect(url_for('.apps'))


@bp.route('/apps/q/ctr')
@developer_only
def ajax_apps_ctr():
	ids = request.args.getlist('id', int)
	stats = actions.stats.get_stats_ctr_by_ids(app_ids=ids, fm=times.delta(datetime.now(), days=-3))
	result = dict([(s.id, dict(actions=s.actions, shows=s.shows, ctr='%.4f' % s.ctr)) for s in stats])
	return jsonify(result)

@bp.route('/orders/q/ctr')
@customer_only
def ajax_orders_ctr():
	ids = request.args.getlist('id', int)
	stats = actions.stats.get_stats_ctr_by_ids(offer_ids=ids, fm=times.delta(datetime.now(), days=-3))
	result = dict([(s.id, dict(actions=s.actions, shows=s.shows, ctr='%.4f' % s.ctr)) for s in stats])
	return jsonify(result)


@bp.route('/orders/<int:id>/stats/q/ctr/')
@customer_only
def ajax_orders_info_stats_ctr(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	return json_get_ctr(offer_id=order.offer_id)

@bp.route('/apps/<int:id>/stats/q/ctr/')
@developer_only
def ajax_apps_info_stats_ctr(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return json_get_ctr(app_id=app.id)

@bp.route('/orders/<int:id>/q/play', methods=['POST'])
@customer_only
def ajax_orders_info_play(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	do_or_abort(actions.orders.play_order, order.id)
	return 'OK'

@bp.route('/orders/<int:id>/q/pause', methods=['POST'])
@customer_only
def ajax_orders_info_pause(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	do_or_abort(actions.orders.pause_order, order.id)
	return 'OK'



