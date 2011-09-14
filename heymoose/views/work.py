# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
import heymoose.forms.forms as forms
from heymoose.views.frontend import frontend
from heymoose.db.models import User
import sys

def fill_template_params(user):
	params = {}
	if not user:
		return params
	params['user_id'] = user.id
	params['user_name'] = user.nickname
	params['balance'] = 100
	return params

@frontend.before_request
def before_request():
	"""Make sure we are connected to the database each request and look
	up the current user so that we know he's there.
	"""
	g.user = None

	#TODO Make it some other way without exception, see LocalProxy object
	g.params = {}
	g.params['loginform'] = forms.LoginForm()

	if 'user_id' in session:
		try:
			g.user = User.get_user_by_id(session['user_id'])
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
			abort(404)
		if g.user:
			g.params.update(fill_template_params(g.user))


@frontend.after_request
def after_request(response):
	"""Closes the database again at the end of the request."""
	return response


def flash_form_errors(errors, type):
	for next in errors:
		for n in next:
			flash(n, type)


