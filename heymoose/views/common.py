# -*- coding: utf-8 -*-
from flask import request, jsonify, send_from_directory, abort
from heymoose import app
from heymoose.utils import convert, times
from heymoose.core import actions
from datetime import datetime

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
		values[replacer(stat.time)] = (stat.shows, stat.actions, stat.ctr)
	
	result = [dict(time=formatter(key), shows=value[0], clicks=value[1], ctr=value[2]) \
				for key, value in sorted(values.items(), key=lambda item: item[0])]
	return jsonify(values=result)


def json_get_audience(**kwargs):
	try:
		fm = convert.to_datetime(request.args.get('from') + ':00')
		to = convert.to_datetime(request.args.get('to') + ':00')
		if fm > to: raise ValueError
	except:
		return u'Неверно указан интервал', 400
	
	
	
	stats_gender = actions.stats.get_stats_actions_by_gender(fm=fm, to=to, **kwargs)
	stats_city = actions.stats.get_stats_actions_by_city(fm=fm, to=to, **kwargs)
	stats_year = actions.stats.get_stats_actions_by_year(fm=fm, to=to, **kwargs)
	
	genders = { True : u'мужчины', False : u'женщины' }
	result_gender = [dict(gender=genders[s.gender], actions=s.actions) for s in stats_gender if s.gender is not None]
	
	top = 8
	others = dict(city=u'другие', actions=0)
	result_city = []
	for s in stats_city:
		if len(result_city) < top and s.city is not None:
			result_city.append(dict(city=s.city, actions=s.actions))
		else:
			others['actions'] += s.actions
	if others['actions'] > 0:
		result_city.append(others)
		
	this_year = datetime.now().year
	result_year = [dict(year=this_year-s.year, actions=s.actions) for s in stats_year if s.year is not None]
	
	result = dict(genders=result_gender, cities=result_city, years=result_year)
	return jsonify(result)


@app.route('/upload/<path:filename>')
def upload(filename):
	if app.config.get('DEBUG', False):
		return send_from_directory(app.config.get('UPLOAD_PATH', ''), filename)
	else:
		abort(403)