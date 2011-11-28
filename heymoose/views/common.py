# -*- coding: utf-8 -*-
from flask import request, jsonify
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