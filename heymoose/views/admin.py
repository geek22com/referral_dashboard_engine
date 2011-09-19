# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
import heymoose.core.actions.actions as actions
from heymoose.views.work import *


@frontend.route('/admin_cabinet', methods = ['POST', 'GET'])
@admin_only
def admin_cabinet():
	if not g.user:
		abort(404)

	actions.get_actions(0, 100)
	if actions:
		g.params['actions'] = actions

	return render_template('admin-cabinet.html', params=g.params)
