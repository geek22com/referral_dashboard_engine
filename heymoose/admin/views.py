from flask import render_template, g, abort
from heymoose.admin import blueprint as bp
from heymoose.core import actions
from heymoose.utils.shortcuts import do_or_abort

#TODO: make paging in user interface
@bp.route('/')
#@admin_only
def index():
	#acs = actions.actions.get_actions(0, 100)
	#if acs: g.params['actions'] = acs

	return render_template('admin/index.html', params=g.params)

@bp.route('/orders/')
def orders():
	ods = actions.orders.get_orders(offset=0, limit=100, full=True)
	return render_template('admin/orders.html', orders=ods)

@bp.route('/orders/stats')
def orders_stats():
	return render_template('admin/orders-stats.html')

@bp.route('/orders/<int:id>')
def orders_info(id):
	order = do_or_abort(actions.orders.get_order, id, full=True)
	return render_template('admin/orders-info.html', order=order)

@bp.route('/orders/<int:id>/stats')
def orders_info_stats(id):
	order = do_or_abort(actions.orders.get_order, id)
	return render_template('admin/orders-info-stats.html', order=order)


@bp.route('/apps/')
def apps():
	aps = do_or_abort(actions.apps.get_apps, offset=0, limit=100, full=True)
	return render_template('admin/apps.html', apps=aps)

@bp.route('/apps/stats')
def apps_stats():
	return render_template('admin/apps-stats.html')

@bp.route('/apps/<int:id>')
def apps_info(id):
	return 'OK'


@bp.route('/customers/<int:id>')
def customers_info(id):
	customer = do_or_abort(actions.users.get_user_by_id, id, full=True)
	if not customer.is_customer(): abort(404)
	return '{0} ({1})'.format(customer.nickname, customer.email)


@bp.route('/developers/<int:id>')
def developers_info(id):
	developer = do_or_abort(actions.users.get_user_by_id, id, full=True)
	if not developer.is_developer(): abort(404)
	return '{0} ({1})'.format(developer.nickname, developer.email)

