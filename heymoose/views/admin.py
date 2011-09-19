# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
import heymoose.core.actions.actions as actions
import heymoose.core.actions.orders as orders
from heymoose.views.work import *

#TODO: make paging in user interface
@frontend.route('/admin_cabinet', methods = ['POST', 'GET'])
@admin_only
def admin_cabinet():
	
	acs = actions.get_actions(0, 100)
	if acs:
		g.params['actions'] = acs

	ods = orders.get_orders(0, 100)
	if ods:
		g.params['orders'] = ods
		
	return render_template('admin-cabinet.html', params=g.params)
