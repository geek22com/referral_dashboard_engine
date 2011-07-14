# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger

from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms

############################ Платежная система heymoose.com #####################################################
#	Функции реализующие платежные операции на сайте heymoose.com
#################################################################################################################

#@frontend.route('/show_balance/<order_id>')
#@auth_only
def show_balance(order_id=None):
	if not order_id:
		return redirect(url_for('main_page'), username=g.user['name'])

	payments = get_paymetns(g.user['id'], order_id)
	if payments:
		g.payments['payments'] = payments

	g.params['order_id'] = order_id
	return render_template('show_balance.html', params=g.params)

#@frontend.route('/pay_balance/<order_id>')
#@auth_only
def pay_balance(order_id=None):
	if not order_id:
		return redirect(url_for('main_page'), username=g.user['name'])

	g.params['order_id'] = order_id
	return render_template('pay_balabce.html', params=g.params)

#@frontend.route('/balance')
#@auth_only
def money_balance():
	if not g.user:
		return redirect(url_for('main_page'))
	params = create_rkass_params(g.user['id']) or {}
	return render_template('balance.html', params = params)

