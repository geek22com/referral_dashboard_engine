# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import developer_only
from heymoose.utils.decorators import customer_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.models import User
from heymoose.utils.workers import app_logger
from heymoose.views.work import flash_form_errors
import sys

def paybalance_form_template(form_params=None, error=None):
	paybalance_form = forms.BalanceForm()
	if form_params:
		paybalance_form.amount.data = form_params['amount']

	g.params['paybalanceform'] = paybalance_form
	return render_template('customer-balance.html', params=g.params)

@frontend.route('/become_developer')
@customer_only
def become_developer():
	if g.user and not g.user.is_developer():
		g.user.become_developer('FACEBOOK')

	return redirect(url_for('user_cabinet', username=g.user.nickname))


@frontend.route('/pay_balance', methods=['GET', 'POST'])
@customer_only
def pay_balance():
	if not g.user:
		abort(404)

	balance_form = forms.BalanceForm(request.form)
	if request.method == 'POST' and balance_form.validate():
		try:
			g.user.increase_balance(balance_form.amount.data)
			return redirect(url_for('user_cabinet', username=g.user.nickname))
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
	

	flash_form_errors(balance_form.errors.values(), 'payerror')
	return paybalance_form_template()

