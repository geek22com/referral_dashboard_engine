# -*- coding: utf-8 -*-
from flask import session, g, flash
from heymoose import app
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.core.actions.users as users
import heymoose.forms.forms as forms
from heymoose.db.actions import captcha

@app.before_request
def before_request():
	g.user = None
	g.performer = None
	g.params = {}
	
	g.params['feedbackform'] = forms.FeedBackForm()
	g.params['feedback_captcha'] = captcha.get_random()
	
	if 'user_id' in session:
		g.user = users.get_user_by_id(session['user_id'], full=True)

	if 'performer_id' in session:
		g.performer = performers.get_performer(session['performer_id'])

@app.after_request
def after_request(response):
	return response


def flash_form_errors(errors, type):
	for next in errors:
		for n in next:
			flash(n, type)


