# -*- coding: utf-8 -*-
from flask import request, jsonify, send_from_directory, abort
from heymoose import app
from heymoose.utils import convert
from heymoose.core.aggregators import ShowsAndClicksAggregator

def json_get_ctr(**kwargs):
	# Check passed GET parameters
	try:
		fm = convert.to_datetime(request.args.get('from') + ':00')
		to = convert.to_datetime(request.args.get('to') + ':00')
		if fm > to: raise ValueError
	except:
		return u'Неверно указан интервал', 400
		
	try:
		group = request.args.get('group')
		if group not in ShowsAndClicksAggregator.config.keys(): raise ValueError
	except:
		return u'Неверно указана группировка', 400
	
	aggregator = ShowsAndClicksAggregator(fm, to, group, **kwargs)
	values = aggregator.aggregate()
	return jsonify(values=values)


@app.route('/upload/<path:filename>')
def upload(filename):
	if app.config.get('DEBUG', False):
		return send_from_directory(app.config.get('UPLOAD_PATH', ''), filename)
	else:
		abort(403)