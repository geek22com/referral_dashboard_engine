# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
import heymoose.forms.forms as forms
from heymoose.views.frontend import frontend
import heymoose.core.actions.users as users
import sys

@frontend.before_request
def before_request():
	g.user = None
	g.params = {}

	if 'user_id' in session:
		g.user = users.get_user_by_id(session['user_id'])


@frontend.after_request
def after_request(response):
	return response


def flash_form_errors(errors, type):
	for next in errors:
		for n in next:
			flash(n, type)


