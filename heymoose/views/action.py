# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.decorators import customer_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.models import Action
from heymoose.db.models import User
from heymoose.views.work import *


@frontend.route('/approve_action/<action_id>', methods = ['POST', 'GET'])
@admin_only
def approve_action(action_id=None):
	action_id = int(action_id)
	if not action_id:
		return redirect(url_for('user_cabinet', username=g.user.nickname))

	try:
		Action.approve(action_id)
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())

	return redirect(url_for('admin_cabinet'))

@frontend.route('/delete_action/<action_id>', methods = ['POST', 'GET'])
@admin_only
def delete_action(action_id=None):
	action_id = int(action_id)
	if not action_id:
		return redirect(url_for('user_cabinet', username=g.user.nickname))

	try:
		Action.delete(action_id)
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())

	return redirect(url_for('admin_cabinet'))

