# -*- coding: utf-8 -*-
from flask import request, jsonify, send_from_directory, abort
from heymoose import app
from heymoose.utils import convert, times
from heymoose.core import actions

def json_get_ctr(**kwargs):
	try:
		fm = convert.to_datetime(request.args.get('from') + ':00')
		to = convert.to_datetime(request.args.get('to') + ':00')
		if fm > to: raise ValueError
	except:
		return u'Неверно указан интервал', 400
		
	try:
		group = request.args.get('group')
		if group not in ('hour', 'day', 'month', 'year'): raise ValueError
	except:
		return u'Неверно указана группировка', 400
	
	if group == 'hour':
		replacer = lambda d: d.replace(minute=0)
		formatter = lambda d: d.strftime('%d.%m.%y') if d.hour == 0 else d.strftime('%H:00')
		freq = times.HOURLY
	elif group == 'day':
		replacer = lambda d: d.replace(minute=0, hour=0)
		formatter = lambda d: d.strftime('%d.%m.%y')
		freq = times.DAILY
	elif group == 'month':
		replacer = lambda d: d.replace(minute=0, hour=0, day=1)
		formatter = lambda d: d.strftime('%m.%y')
		freq = times.MONTHLY
	elif group == 'year':
		replacer = lambda d: d.replace(minute=0, hour=0, day=1, month=1)
		formatter = lambda d: d.strftime('%y')
		freq = times.YEARLY
		
	fm = replacer(fm); to = replacer(to)
	keys = times.datetime_range(freq, dtstart=fm, until=to)
	values = dict([(key, (0, 0, 0.0)) for key in keys])
	stats = actions.stats.get_stats_ctr(fm, to, group, **kwargs)
	for stat in stats:
		values[stat.time] = (stat.shows, stat.actions, stat.ctr)
	
	result = [dict(time=formatter(key), shows=value[0], clicks=value[1], ctr=value[2]) \
				for key, value in sorted(values.items(), key=lambda item: item[0])]
	return jsonify(values=result)


@app.route('/upload/<path:filename>')
def upload(filename):
	if app.config.get('DEBUG', False):
		return send_from_directory(app.config.get('UPLOAD_PATH', ''), filename)
	else:
		abort(403)