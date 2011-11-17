from flask import render_template, g, request
from heymoose import app
from heymoose.admin import blueprint as bp
from heymoose.core import actions as a
from heymoose.utils import convert
from heymoose.utils.shortcuts import do_or_abort, paginate


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

@bp.route('/orders/<int:id>')
def orders_info(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	return render_template('admin/orders-info.html', order=order)

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


@bp.route('/orders/<int:id>/q/enable', methods=['POST'])
def ajax_orders_enable(id):
	do_or_abort(a.orders.enable_order, id)
	return 'OK'

@bp.route('/orders/<int:id>/q/disable', methods=['POST'])
def ajax_orders_disable(id):
	do_or_abort(a.orders.disable_order, id)
	return 'OK'


