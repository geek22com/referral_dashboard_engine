from flask import render_template, g, request, abort, jsonify
from heymoose import app
from heymoose.admin import blueprint as bp
from heymoose.core import actions as a
from heymoose.core.actions import performers as perf
from heymoose.core.actions import shows as sh
from heymoose.utils import convert, times
from heymoose.utils.shortcuts import do_or_abort, paginate
import random


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

@bp.route('/orders/<int:id>/')
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


@bp.route('/performers/')
def performers():
	page = convert.to_int(request.args.get('page'), 1)
	count = perf.get_performers_count()
	per_page = app.config.get('ADMIN_PERFORMERS_PER_PAGE', 20)
	offset, limit, pages = paginate(page, count, per_page)
	perfs = do_or_abort(perf.get_performers, offset=offset, limit=limit, full=True)
	return render_template('admin/performers.html', performers=perfs, pages=pages)

@bp.route('/performers/stats')
def performers_stats():
	return render_template('admin/performers-stats.html')

@bp.route('/performers/<int:id>')
def performers_info(id):
	performer = do_or_abort(perf.get_performer, id, full=True)
	return render_template('admin/performers-info.html', performer=performer)

@bp.route('/performers/<int:id>/stats')
def performers_info_stats(id):
	performer = do_or_abort(perf.get_performer, id, full=True)
	return render_template('admin/performers-info-stats.html', performer=performer)


@bp.route('/orders/<int:id>/q/enable', methods=['POST'])
def ajax_orders_enable(id):
	do_or_abort(a.orders.enable_order, id)
	return 'OK'

@bp.route('/orders/<int:id>/q/disable', methods=['POST'])
def ajax_orders_disable(id):
	do_or_abort(a.orders.disable_order, id)
	return 'OK'

@bp.route('/orders/<int:id>/stats/q/ctr/')
def ajax_orders_info_stats_ctr(id):
	order = do_or_abort(a.orders.get_order, id, full=True)
	
	# Some parameters for aggregation
	config = dict(
		minute = dict(
			format=lambda d: d.strftime('%d.%m.%y') if d.hour == 0 and d.minute == 0 else d.strftime('%H:%M'), 
			freq=times.MINUTELY),
		hour = dict(
			format=lambda d: d.strftime('%d.%m.%y') if d.hour == 0 and d.minute == 0 else d.strftime('%H:00'),
			freq=times.HOURLY),
		day = dict(
			format=lambda d: d.strftime('%d.%m.%y'),
			freq=times.DAILY),
		month = dict(
			format=lambda d: d.strftime('%m.%y'),
			freq=times.MONTHLY)
	)
	
	# Check passed GET parameters
	try:
		fm = convert.to_datetime(request.args.get('from') + ':00')
		to = convert.to_datetime(request.args.get('to') + ':00')
		if fm > to: raise ValueError
		
		group = request.args.get('group')
		if group not in config.keys(): raise ValueError
	except:
		abort(400)
		
	conf = config[group]
	format = conf['format']		# Current datetime formatting function
	freq = conf['freq']			# Current frequency
	# Hack for obtaining functions for appropriate time period
	fbegin = getattr(times, 'begin_of_{0}'.format(group))
	fend = getattr(times, 'end_of_{0}'.format(group))
	# Align entered datetimes by current group
	dtbegin = fbegin(fm)
	dtend = fend(to)
	
	# Generate some test random data
	checkpoints = times.datetime_range(times.MINUTELY, dtstart=dtbegin, until=dtend)
	clicks = [random.choice(checkpoints) for _x in range(10)]
	#shows = [random.choice(checkpoints) for _x in range(10000)]
	shows = sh.get_shows_range(dtbegin, dtend, offerId=order.id) # TODO: need offer_id
	
	# List of all times in interval with period depending on group
	keys = times.datetime_range(freq, dtstart=dtbegin, until=dtend)
	
	# Fill result dict with test data
	result = dict([(key, [0, 0]) for key in keys])
	for click in clicks: result[fbegin(click)][0] += 1
	for show in shows: result[fbegin(show.show_time)][1] += 1
	
	# This magic expression transforms dict to list of dicts sorted by datetime	
	json_result = [dict(time=format(key), clicks=value[0], shows=value[1]) \
						for key, value in sorted(result.items(), key=lambda item: item[0])]
	return jsonify(values=json_result)


