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
		replacer = times.begin_of_hour
		formatter = lambda d: d.strftime('%d.%m.%y') if d.hour == 0 else d.strftime('%H:00')
		freq = times.HOURLY
	elif group == 'day':
		replacer = times.begin_of_day
		formatter = lambda d: d.strftime('%d.%m.%y')
		freq = times.DAILY
	elif group == 'month':
		replacer = times.begin_of_month
		formatter = lambda d: d.strftime('%m.%Y')
		freq = times.MONTHLY
	elif group == 'year':
		replacer = times.begin_of_year
		formatter = lambda d: d.strftime('%Y')
		freq = times.YEARLY
		
	#fm = replacer(fm)
	#to = replacer(to)
	stats = actions.stats.get_stats_ctr(fm, to, group, **kwargs)
	keys = times.datetime_range(freq, dtstart=replacer(fm), until=replacer(to))
	values = dict([(key, (0, 0, 0.0)) for key in keys]) # if len(stats) != len (keys) else dict()
	for stat in stats:
		print stat.time
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