# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.decorators import customer_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.views.work import *


@frontend.route('/admin_cabinet', methods = ['POST', 'GET'])
@admin_only
def admin_cabinet():
	if not g.user:
		abort(404)

	try:
		actions = Action.load_actions(0, 100)
		if actions:
			g.params['actions'] = actions
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return redirect(url_for('main_page'))

	return render_template('admin-cabinet.html', params=g.params)
