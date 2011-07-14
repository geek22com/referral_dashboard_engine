# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.models import Order
from heymoose.views.work import *

def order_form_template(form_params=None):
	order_form = forms.OrderForm()
	if form_params:
		order_form.ordername.data = form_params['ordername']
		order_form.orderbalance.data = form_params['orderbalance']
		order_form.orderquestions.data = form_params['orderquestions']

	g.params['orderform'] = order_form
	return render_template('order-creation-form.html', params = g.params)

@frontend.route('/create_order', methods=['POST'])
@auth_only
def create_order():
	#TODO проверка данных
	order_form = forms.OrderForm(request.form)
	if request.method == "POST" and order_form.validate():
		order = Order(owner_id = g.user.userid,
					title = order_form.ordername.data,
					balance = order_form.orderbalance.data,
					body = order_form.orderquestions.data)
		try:
			order.save_new()
		except:
			pass
		return redirect(url_for('user_cabinet', username=g.user.username))

	flash_form_errors(order_form.errors.values(), 'ordererror')
	return order_form_template(request.form)

#TODO: Make it more simple, use AJAX for all forms
@frontend.route('/order/<order_id>', methods = ['POST', 'GET'])
@auth_only
def show_order(order_id=None):
	if not order_id:
		return redirect(url_for('user_cabinet', username=g.user.username))

	order = Order.load_order(g.user.userid, order_id)
	order_form = forms.OrderForm()
	if order:
		g.params['order'] = order
		order_form.ordername.data = order.title
		order_form.orderbalance.data = order.balance
		order_form.orderquestions.data = order.body
	else:
		return redirect(url_for('user_cabinet', username=g.user.username))

	if request.method == "POST":
		order_form = forms.OrderForm(request.form)
		if order_form.validate():
			order = Order(owner_id = g.user.userid,
						title = order_form.ordername.data,
						balance = order_form.orderbalance.data,
						body = order_form.orderquestions.data)
			try:
				order.save(order_id)
			except:
				pass
			return redirect(url_for('user_cabinet', username=g.user.username))
		flash_form_errors(order_form.errors.values(), 'ordererror')

	g.params['orderform'] = order_form
	return render_template('cabinet-questionlist.html', params=g.params)

@frontend.route('/delete_order/<order_id>')
@auth_only
def delete_order(order_id):
	if not order_id:
		abort(404)
	Order.delete_order(order_id)
	return redirect(url_for('user_cabinet', username=g.user.username))

@frontend.route('/order_form', methods=['POST', 'GET'])
@auth_only
def order_form():
	if request.method == 'POST':
		file = request.files['questionlist']
		if file:
			g.params['questionlist'] = file.stream.read().decode('utf8')
	return order_form_template()

