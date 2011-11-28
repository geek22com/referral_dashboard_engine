# -*- coding: utf-8 -*-
import base64
from flask import request, url_for, redirect, render_template
from heymoose.utils.decorators import auth_only, admin_only, customer_only
import heymoose.forms.forms as forms
import heymoose.core.actions.orders as orders
from heymoose.views.work import *

def order_form_template(form_params=None):
	order_form = forms.OrderForm()
	if form_params:
		order_form.ordername.data = form_params['ordername']
		order_form.orderdesc.data = form_params['orderdesc']
		order_form.orderbalance.data = form_params['orderbalance']
		order_form.orderbody.data = form_params['orderbody']
		order_form.ordercpa.data = form_params['ordercpa']
	
	g.params['orderform'] = order_form
	return render_template('new-create-order.html', params = g.params)
'''
@frontend.route('/cabinet/orders/')
@auth_only
def cabinet_orders():
	return render_template('cabinet_orders.html', orders=g.user.orders)

@frontend.route('/cabinet/create_order', methods=['POST', 'GET'])
@customer_only
def create_order():
	#TODO проверка данных
	order_form = forms.OrderForm(request.form)
	if request.method == "POST" and order_form.validate():
		file = request.files['orderimage']
		image_data = file.stream.read()
	
		orders.add_order(user_id=g.user.id,
	                    title=order_form.ordername.data,
	                    url=order_form.orderbody.data,
	                    balance = order_form.orderbalance.data,
	                    cpa=order_form.ordercpa.data,
	                    desc=order_form.orderdesc.data,
	                    image_data=base64.encodestring(image_data).strip('\n'),
	                    autoApprove=order_form.orderautoaprove.data,
	                    allowNegativeBalance=order_form.orderallownegativebalance.data,
	                    male=order_form.ordermale.data,
	                    minAge=order_form.orderminage.data,
	                    maxAge=order_form.ordermaxage.data)
		return redirect(url_for('user_cabinet'))
	
	flash_form_errors(order_form.errors.values(), 'ordererror')
	return order_form_template(request.form)
'''


@frontend.route('/delete_order/<order_id>')
@customer_only
def delete_order(order_id):
	return redirect(url_for('user_cabinet'))

@frontend.route('/order_form', methods=['POST', 'GET'])
@customer_only
def order_form():
	if request.method == 'POST':
		pass
		#file = request.files['questionlist']
		#if file:
			#g.params['questionlist'] = file.stream.read().decode('utf8')
	return order_form_template()

@frontend.route('/approve_order/<order_id>', methods = ['POST', 'GET'])
@admin_only
def approve_order(order_id=None):
	order_id = int(order_id)
	if not order_id:
		return redirect(url_for('user_cabinet'))

	orders.approve_order(order_id)
	return redirect(url_for('admin.index'))
