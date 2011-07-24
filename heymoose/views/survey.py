# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms

@frontend.route('/create_survey/<app_id>')
def create_survey(app_id=None):
	if not app_id:
		abort(404)
	try:
		app_id = int(app_id)
	except:
		abort(404)

	return render_template('survey-offer.html', params=g.params)
