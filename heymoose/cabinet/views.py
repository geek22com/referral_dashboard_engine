# -*- coding: utf-8 -*-
from flask import render_template, g, redirect, url_for, abort, request, flash
from heymoose import app
from heymoose.cabinet import blueprint as bp
from heymoose.forms import forms
from heymoose.core import actions
from heymoose.core.data import OrderTypes
from heymoose.utils import convert
from heymoose.utils.shortcuts import do_or_abort
from heymoose.utils.gen import generate_password_hash
from heymoose.views.common import json_get_ctr
from decorators import customer_only, developer_only
import base64


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
	return render_template('cabinet/orders.html', orders=g.user.orders)

@bp.route('/orders/new', methods=['GET', 'POST'])
@customer_only
def orders_new():
	sizes = actions.bannersizes.get_banner_sizes()
	choices = [(s.id, '{0} x {1}'.format(s.width, s.height)) for s in sizes]
	cities = [dict(id=city.id, name=city.name) for city in actions.cities.get_cities()]
	
	ordertype = 'REGULAR'
	rform = forms.RegularOrderForm()
	bform = forms.BannerOrderForm()
	vform = forms.VideoOrderForm()
	bform.orderbannersize.choices = choices
	
	if request.method == 'POST':
		ordertype = request.form['ordertype']
		if ordertype == OrderTypes.REGULAR:
			form = forms.RegularOrderForm(request.form)
			rform = form
		elif ordertype == OrderTypes.BANNER:
			form = forms.BannerOrderForm(request.form)
			form.orderbannersize.choices = choices
			bform = form
		elif ordertype == OrderTypes.VIDEO:
			form = forms.VideoOrderForm(request.form)
			vform = form
		else:
			abort(400)
			
		if form.validate():
			kwargs = dict(
				user_id=g.user.id,
				title=form.ordername.data,
				url=form.orderurl.data,
				balance=form.orderbalance.data,
				cpa=form.ordercpa.data,
				auto_approve=form.orderautoapprove.data,
				allow_negative_balance=form.orderallownegativebalance.data,
				reentrant=form.orderreentrant.data,
				male=form.ordermale.data,
				min_age=form.orderminage.data,
				max_age=form.ordermaxage.data,
				city_filter_type=form.ordercitiesfilter.data,
				city=[int(x) for x in form.ordercities.data.split(',')] if form.ordercities.data else []
			)
			
			if ordertype == OrderTypes.REGULAR:
				kwargs.update(
					description=form.orderdesc.data,
					image=base64.encodestring(request.files['orderimage'].stream.read())
				)
				do_or_abort(actions.orders.add_regular_order, **kwargs)
			elif ordertype == OrderTypes.BANNER:
				kwargs.update(
					banner_size=form.orderbannersize.data,
					image=base64.encodestring(request.files['orderimage'].stream.read())
				)
				do_or_abort(actions.orders.add_banner_order, **kwargs)
			elif ordertype == OrderTypes.VIDEO:
				kwargs.update(video_url=form.ordervideourl.data) 
				do_or_abort(actions.orders.add_video_order, **kwargs)

			flash(u'Заказ успешно создан.', 'success')
			return redirect(url_for('.orders'))
	
	return render_template('cabinet/orders-new.html', 
		rform=rform, bform=bform, vform=vform, cities=cities,
		ordertype=ordertype.lower())
	
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
			actions.orders.add_order_banner(order.id, form.size.data,
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
		orderbalance = order.balance,
		ordercpa = order.cpa,
		orderautoapprove = order.auto_approve,
		orderreentrant = order.reentrant,
		orderallownegativebalance = order.allow_negative_balance,
		ordermale = u'' if order.male is None else unicode(order.male),
		orderminage = order.min_age,
		ordermaxage = order.max_age,
		ordercitiesfilter = order.city_filter_type
	)
	
	if order.is_regular():
		form_args.update(orderdesc = order.description)
		form = forms.RegularOrderForm(request.form, **form_args)
		form.orderimage.validators = form.orderimage.validators[:]
		del form.orderimage.validators[0] # Remove Required validator
	elif order.is_banner():
		form_args.update(orderbannersize = order.banner_size.id)
		form = forms.BannerOrderForm(request.form, **form_args)
		form.orderimage.validators = form.orderimage.validators[:]
		del form.orderimage.validators[0] # Remove Required validator
		
		sizes = actions.bannersizes.get_banner_sizes()
		choices = [(s.id, '{0} x {1}'.format(s.width, s.height)) for s in sizes]
		form.orderbannersize.choices = choices
	elif order.is_video():
		form_args.update(ordervideourl = order.video_url)
		form = forms.VideoOrderForm(request.form, **form_args)
		
	form.orderbalance.validators = []
		
	if request.method == 'POST' and form.validate():
		kwargs = dict()
		male = convert.to_bool(form.ordermale.data)
		city_filter_type = form.ordercitiesfilter.data if form.ordercitiesfilter.data else None
		
		if form.ordername.data != order.title: kwargs.update(title=form.ordername.data)
		if form.orderurl.data != order.url: kwargs.update(url=form.orderurl.data)
		#if form.ordercpa.data != order.cpa: kwargs.update(cpa=form.ordercpa.data)
		if form.orderautoapprove.data != order.auto_approve: kwargs.update(auto_approve=form.orderautoapprove.data)
		if form.orderreentrant.data != order.reentrant: kwargs.update(reentrant=form.orderreentrant.data)
		if form.orderallownegativebalance.data != order.allow_negative_balance: kwargs.update(allow_negative_balance=form.orderallownegativebalance.data)
		if male != order.male: kwargs.update(male=male)
		if form.orderminage.data != order.min_age: kwargs.update(min_age=form.orderminage.data)
		if form.ordermaxage.data != order.max_age: kwargs.update(max_age=form.ordermaxage.data)
		if city_filter_type != order.city_filter_type: kwargs.update(city_filter_type=city_filter_type)
		
		old_cities = frozenset([city.id for city in order.cities])
		new_cities = frozenset([int(x) for x in form.ordercities.data.split(',')] if form.ordercities.data else [])
		if new_cities != old_cities: kwargs.update(city=list(new_cities))
				
		if order.is_regular():
			if form.orderdesc.data != order.description: kwargs.update(description=form.orderdesc.data)
			if form.orderimage.data is not None: kwargs.update(image=base64.encodestring(request.files['orderimage'].stream.read()))
		elif order.is_banner():
			if form.orderimage.data is not None:
				kwargs.update(image=base64.encodestring(request.files['orderimage'].stream.read()))
				if form.orderbannersize.data != order.banner_size.id: kwargs.update(banner_size=form.orderbannersize.data)
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

@bp.route('/orders/<int:id>/stats')
@customer_only
def orders_info_stats(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	return render_template('cabinet/orders-info-stats.html', order=order)
	

@bp.route('/apps/')
@developer_only
def apps():
	return render_template('cabinet/apps.html', apps=g.user.apps)

@bp.route('/apps/new', methods=['GET', 'POST'])
@developer_only
def apps_new():
	form = forms.AppForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.apps.add_app,
			title=form.apptitle.data,
			user_id=g.user.id,
			callback=form.appcallback.data,
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

#@bp.route('/info/balance/pay', methods=['GET', 'POST'])
@customer_only
def balance_pay():
	'''Deprecated: now in admin blueprint'''
	form = forms.BalanceForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(actions.users.increase_customer_balance,
				g.user.id, int(form.amount.data))
		flash(u'Баланс успешно пополнен', 'success')
		return redirect(url_for('.info'))
	return render_template('cabinet/info-balance-pay.html', form=form) 
	

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


@bp.route('/orders/<int:id>/stats/q/ctr/')
@customer_only
def ajax_orders_info_stats_ctr(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	if order.user.id != g.user.id: abort(404)
	return json_get_ctr(offerId=order.offer_id)

@bp.route('/apps/<int:id>/stats/q/ctr/')
@developer_only
def ajax_apps_info_stats_ctr(id):
	app = do_or_abort(actions.apps.get_app, id, full=True)
	if app.user.id != g.user.id: abort(404)
	return json_get_ctr(appId=app.id)




