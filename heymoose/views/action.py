# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.core.data import Action
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.decorators import customer_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.views.work import *
import heymoose.core.actions.actions as actions

@frontend.route('/approve_action/<action_id>', methods = ['POST', 'GET'])
@admin_only
def approve_action(action_id=None):
	action_id = int(action_id)
	if not action_id:
		return redirect(url_for('user_cabinet'))

	actions.approve_action(action_id)
	return redirect(url_for('admin.index'))

@frontend.route('/delete_action/<action_id>', methods = ['POST', 'GET'])
@admin_only
def delete_action(action_id=None):
	action_id = int(action_id)
	if not action_id:
		return redirect(url_for('user_cabinet'))

	actions.delete_action(action_id)
	return redirect(url_for('admin.index'))

