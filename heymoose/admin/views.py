# -*- coding: utf-8 -*-
from flask import render_template, g, request, abort, redirect, flash, url_for, jsonify
from heymoose import app
from heymoose.admin import blueprint as bp
from heymoose.core import actions as a
from heymoose.core.actions import roles
from heymoose.utils import convert, gen
from heymoose.utils.shortcuts import do_or_abort, paginate
from heymoose.views.common import json_get_ctr
from heymoose.forms import forms
from heymoose.db.models import Contact
from heymoose.db.actions import invites


@bp.route('/')
def index():
	return render_template('admin/index.html', params=g.params)


@bp.route('/orders/')
def orders():
	page = convert.to_int(request.args.get('page'), 1)
	count = a.orders.get_orders_count()
	per_page = app.config.get('ADMIN_ORDERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	print offset, limit, pages
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

@bp.route('/orders/<int:id>/')
def orders_info(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return render_template('admin/orders-info.html', order=order)

@bp.route('/orders/<int:id>/banners')
def orders_info_banners(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	if not order.is_banner(): abort(404)
	return render_template('admin/orders-info-banners.html', order=order)

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

@bp.route('/orders/<int:id>/stats')
def orders_info_stats(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return render_template('admin/orders-info-stats.html', order=order)


@bp.route('/apps/')
def apps():
	page = convert.to_int(request.args.get('page'), 1)
	count = a.apps.get_apps_count()
	per_page = app.config.get('ADMIN_APPS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	aps = do_or_abort(a.apps.get_apps, offset=offset, limit=limit, full=True)
	return render_template('admin/apps.html', apps=aps, pages=pages)

@bp.route('/apps/stats')
def apps_stats():
	return render_template('admin/apps-stats.html')

@bp.route('/apps/<int:id>')
def apps_info(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return render_template('admin/apps-info.html', app=app)

@bp.route('/apps/<int:id>/actions')
def apps_info_actions(id):
	ap = do_or_abort(a.apps.get_app, id, full=True)
	page = convert.to_int(request.args.get('page'), 1)
	count = a.actions.get_actions_count(appId=ap.id)
	per_page = app.config.get('ADMIN_ACTIONS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	acts = do_or_abort(a.actions.get_actions, offset=offset, limit=limit, full=True, appId=ap.id)
	return render_template('admin/apps-info-actions.html', app=ap, actions=acts, pages=pages)

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

@bp.route('/users/invites')
def users_invites():
	return render_template('admin/users-invites.html')

@bp.route('/users/register/customer', methods=['GET', 'POST'])
def users_register_customer():
	form = forms.CustomerRegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(a.users.add_user,
			email=form.email.data,
			passwordHash=gen.generate_password_hash(form.password.data),
			nickname=form.username.data)
		user = do_or_abort(a.users.get_user_by_email, form.email.data, full=True)
		if user:
			a.users.add_user_role(user.id, roles.CUSTOMER)
			flash(u'Рекламодатель успешно зарегистрирован', 'success')
			return redirect(url_for('.users_info', id=user.id))
		flash(u'Произошла ошибка при регистрации. Обратитесь к администрации.', 'error')
	
	return render_template('admin/users-register-customer.html', form=form)

@bp.route('/users/stats')
def users_stats():
	return render_template('admin/users-stats.html')

@bp.route('/users/<int:id>')
def users_info(id):
	user = do_or_abort(a.users.get_user_by_id, id, full=True)
	return render_template('admin/users-info.html', user=user)

@bp.route('/users/<int:id>/stats')
def users_info_stats(id):
	user = do_or_abort(a.users.get_user_by_id, id, full=True)
	return render_template('admin/users-info-stats.html', user=user)

@bp.route('/users/<int:id>/orders')
def users_info_orders(id):
	user = do_or_abort(a.users.get_user_by_id, id, full=True)
	if not user.is_customer(): abort(404)
	return render_template('admin/users-info-orders.html', user=user)

@bp.route('/users/<int:id>/apps')
def users_info_apps(id):
	user = do_or_abort(a.users.get_user_by_id, id, full=True)
	if not user.is_developer(): abort(404)
	return render_template('admin/users-info-apps.html', user=user)

@bp.route('/users/<int:id>/password', methods=['GET', 'POST'])
def users_info_password_change(id):
	user = do_or_abort(a.users.get_user_by_id, id, full=True)
	form = forms.AdminPasswordChangeForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(a.users.update_user, user.id,
			gen.generate_password_hash(form.password.data))
		flash(u'Пароль пользователя успешно изменен', 'success')
		return redirect(url_for('.users_info', id=user.id))
	return render_template('admin/users-info-password-change.html', user=user, form=form)

@bp.route('/users/<int:id>/balance/pay', methods=['GET', 'POST'])
def balance_pay(id):
	user = do_or_abort(a.users.get_user_by_id, id, full=True)
	if not user.is_customer(): abort(404)
	
	form = forms.BalanceForm(request.form)
	if request.method == 'POST' and form.validate():
		do_or_abort(a.users.increase_customer_balance,
				user.id, int(form.amount.data))
		flash(u'Баланс успешно пополнен', 'success')
		return redirect(url_for('.users_info', id=user.id))
	return render_template('admin/users-info-balance-pay.html', user=user, form=form) 


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


@bp.route('/feedback/', methods=['GET', 'POST'])
def feedback():
	if request.method == 'POST':
		contacts = Contact.query.filter(Contact.read == False)
		for contact in contacts: # For some reason set/execute query not working
			contact.read = True
			contact.save()
		g.feedback_unread = 0
	
	page = convert.to_int(request.args.get('page'), 1)
	count = Contact.query.count()
	per_page = app.config.get('ADMIN_CONTACTS_PER_PAGE', 10)
	offset, limit, pages = paginate(page, count, per_page)
	contacts = Contact.query.descending(Contact.date).skip(offset).limit(limit)
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


@bp.route('/orders/<int:id>/stats/q/ctr/')
def ajax_orders_info_stats_ctr(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return json_get_ctr(offer_id=order.offer_id)

@bp.route('/apps/<int:id>/stats/q/ctr/')
def ajax_apps_info_stats_ctr(id):
	app = do_or_abort(a.apps.get_app, id, full=True)
	return json_get_ctr(app_id=app.id)

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
	


