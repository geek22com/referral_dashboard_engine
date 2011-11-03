# -*- coding: utf-8 -*-
from flask import session, g, flash
from heymoose import app
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.core.actions.users as users

@app.before_request
def before_request():
	g.user = None
	g.performer = None
	g.params = {}
	if 'user_id' in session:
		g.user = users.get_user_by_id(session['user_id'])

	if 'performer_id' in session:
		g.performer = performers.get_performer(session['performer_id'])

@app.after_request
def after_request(response):
	return response


def flash_form_errors(errors, type):
	for next in errors:
		for n in next:
			flash(n, type)


