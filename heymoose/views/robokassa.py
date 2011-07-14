# -*- coding: utf-8 -*-
# Платежи не работают.
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms

PAYMENT_STATUS = {'result' : 1,
				'succes' : 2,
				'xml_checked': 3,
				'fail' : -1}

############################ Агрегатор платяжей робокасса ######################################################
#	Реализация функций работы с робокассой
#	Документация: http://www.robokassa.ru/ru/HowTo.aspx
#################################################################################################################
def get_rkass_login():
	query = "SELECT * FROM robokassa"
	res = query_db(query)
	return res['login'].decode('utf8')

def get_rkass_pass(type=None):
	pass_str = "pass" + str(type)
	query = "SELECT * FROM robokassa"
	res = query_db(query)
	return res[pass_str].decode('utf8')

def get_rkass_balance_name(user_id):
	return "Пополните ваш баланс:"

def get_rkass_product_type(type=None):
	if type == 'balance':
		return 0
	return None

def get_rkass_default_cur(type=None):
	return "AlfaBankR"

def get_rkass_language(user_id=None):
	return "ru"

def get_rkass_crc_string(login=None, summ=None, inv_id=None, rkass_pass=None, shp_item=None):
	if not rkass_pass:
		return None
	# $mrh_login:$out_summ:$inv_id:$mrh_pass1:Shp_item=$shp_item
	order = str(login) + ":" + str(summ) + ":" + str(inv_id) + ":" + str(rkass_pass) + ":" + "Shp_item=" + str(shp_item)
	crc = md5(order)
	return crc.hexdigest()

def get_rkass_server_url():
	query = "SELECT * FROM robokassa"
	res = query_db(query)
	return res['server_url'].decode('utf8')


def create_rkass_params(user_id):
	params = {}

	rkass_login = get_rkass_login();
	rkass_pass1 = get_rkass_pass(type="1");
	if not (rkass_login and rkass_pass1):
		return None

	inv_id = 0;
	inv_desc = get_rkass_balance_name(user_id);
	out_summ = "";

	shp_item = get_rkass_product_type(type='balance');
	in_curr = get_rkass_default_cur(type='balance');
	culture = get_rkass_language(user_id=user_id);
	crc = get_rkass_crc_string(login=rkass_login,
							   summ=out_summ,
							   inv_id=inv_id,
							   rkass_pass=rkass_pass1,
							   shp_item=shp_item)
	params['rkass_login'] = rkass_login
	params['out_summ'] = out_summ
	params['inv_id'] = inv_id
	params['inv_desc'] = inv_desc
	params['rkass_crc'] = crc
	params['shp_item'] = shp_item
	params['in_curr'] = in_curr
	params['rkass_culture'] = culture
	params['rkass_url'] = get_rkass_server_url()

	return params

#@frontend.route('/exec_payment', methods=['POST'])
#@auth_only
def exec_payment():
	if request.method == 'POST':
		order_id = request.form['order_id']
		payment_url = get_rkass_server_url()
		if not payment_url:
			return redirect(url_for('error_page'))

		payment_url += serialize_rkass_params(g.user, order_id)
		if payment_url:
			return redirect(payment_url)
		else:
			return redirect(url_for('error_page'))

#@frontend.route('/robo_result', methods=['POST'])
#@auth_only
def robo_result():
	if request.method == 'POST':
		params = deserialize_rkass_params(g.user, request.form)
		if params:
			change_payment_status(params['payment_id'], PAYMENT_STATUS['result'])
			return params['ok']
		else:
			return 'Fail'

#@frontend.route('/robo_fail', methods=['POST'])
#@auth_only
def robo_fail():
	if request.method == 'POST':
		params = deserialize_rkass_params(g.user, request.form)
		if params:
			change_payment_status(params['payment_id'], PAYMENT_STATUS['fail'])
			return params['ok']
		else:
			return 'Fail'

#@frontend.route('/robo_success', methods=['GET' ,'POST'])
#@auth_only
def robo_success():
	if request.method == 'POST':
		params = deserialize_rkass_params(g.user, request.form)
		if params:
			g.params['payment'] = params
			change_payment_status(params['payment_id'], PAYMENT_STATUS['success'])
			check_xml = check_rkass_payment(params['payment_id'])
			if check_xml:
				change_payment_status(params['payment_id'], PAYMENT_STATUS['xml_checked'])

	return render_template('payment_success.html', params=g.params)


