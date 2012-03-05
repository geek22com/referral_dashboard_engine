# -*- coding: utf-8 -*-
from flask import request, abort, send_from_directory
from heymoose import app
from heymoose.db.models import DummyAction
from datetime import datetime

@app.route('/test-api/')
def test_api():
	method = request.args.get('method', None)
	method_handler = {
		'reportAction': report_action
	}.get(method, None)
	
	if not method_handler:
		abort(400)
	return method_handler()


def report_action():
	try:
		offer_id = int(request.args.get('offer_id', None))
	except (TypeError, ValueError):
		abort(400)
	
	action = DummyAction.query.get_or_create(offer_id=offer_id)
	action.date = datetime.now()
	action.save()
	
	response = send_from_directory(app.static_folder, filename='img/px/px.png', cache_timeout=0)
	response.cache_control.no_cache = True
	return response