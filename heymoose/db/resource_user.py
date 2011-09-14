from http import api_request
from http import dumps
from http import response_to_dict
from heymoose.utils.workers import app_logger
from xml_parser import xpath_to_string
from resource_order import order_to_dict
from resource_order import construct_orders_from_xml
from resource_app import construct_apps_from_xml
from lxml import etree

import sys

resource_path = "/users"
user_roles = {}
user_roles['DEVELOPER'] = 'DEVELOPER'
user_roles['CUSTOMER'] = 'CUSTOMER'
user_roles['ADMIN'] = 'ADMIN'

#TODO: remove functions ...(xml_string) and make it more generic, (e.x. object)

def create_role(role):
	lst = []
	lst.append(role)
	return lst

def get_customer_balance(xml_string):
	try:
		res = xpath_to_string(xml_string, '/user/customer-account')

		if res:
			return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		
	return None

def get_developer_balance(xml_string):
	try:
		res = xpath_to_string(xml_string, '/user/developer-account')

		if res:
			return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())

	return None


def get_roles(xml_string):
	try:
		res = []
		root = etree.fromstring(xml_string)
		roles = root.find('roles')
		if len(roles):
			for role in roles:
				item = role.text
				if item:
					res.append(item)
		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def construct_user_from_xml(xml_string): # it is work:)) Maybe we should use json instead?
	if not xml_string:
		return None

	try:
		res = {}
		res['email'] = xpath_to_string(xml_string, '/user/email')
		res['nickname'] = xpath_to_string(xml_string, '/user/nickname')
		res['passwordHash'] = xpath_to_string(xml_string, '/user/password-hash')
		res['id'] = xpath_to_string(xml_string, '@id')

		roles = get_roles(xml_string)
		if roles:
			res['roles'] = roles
			if user_roles['CUSTOMER'] in roles:
				orders = construct_orders_from_xml(xml_string)
				if orders:
					res['orders'] = orders
				customer_balance = get_customer_balance(xml_string)
				if customer_balance:
					res['customer_balance'] = customer_balance
			if user_roles['DEVELOPER'] in roles:
				apps = construct_apps_from_xml(xml_string)
				if apps:
					res['apps'] = apps
				developer_balance = get_developer_balance(xml_string)
				if developer_balance:
					res['developer_balance'] = developer_balance

		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None


def get_user_orders(user_id):
	path = resource_path + "/" + str(user_id)
	response = api_request(path=path)

	app_logger.debug("load_orders " + path)
	return response_to_dict(response, func=construct_orders_from_xml)

def set_user_role(user_id, role):
	path = resource_path + "/" + str(user_id)
	data = dict(role=role)
	payload=dumps(data)

	app_logger.debug("set_user_role " + path + payload)
	return api_request(path=path, payload=payload, type="PUT")

def become_developer(user_id):
	return set_user_role(user_id, user_roles['DEVELOPER'])

def become_customer(user_id):
	return set_user_role(user_id, user_roles['CUSTOMER'])


def add_user(email, password, nickname):
	path = resource_path
	data = dict(email=email, passwordHash=password, nickname=nickname)
	payload=dumps(data)

	app_logger.debug("add_user " + path)
	return api_request(path=path, payload=payload, type="POST")

def get_user_by_id(id):
	path = resource_path + "/" + str(id)    #TODO: make generic parameters build
	params = {'full' : 'true'} #TODO: make it false later
	response = api_request(path=path, params_dict=params)

	app_logger.debug("get_user_by_id " + path)
	return response_to_dict(response, func=construct_user_from_xml)

def get_user_by_email(email):
	path = resource_path #TODO: make generic parameters build
	params = {'email' : email, 'full' : 'true'}
	response = api_request(path=path, params_dict=params)

	app_logger.debug("get_user_by_email" + path)
	return response_to_dict(response, func=construct_user_from_xml)

def increase_customer_account(user_id, amount):
	path = resource_path + "/" + str(user_id) + "/" + "customer-account"
	data = dict(amount=amount)
	payload=dumps(data)

	app_logger.debug("increase_customer_account" + path)
	return api_request(path=path, payload=payload, type="PUT")
