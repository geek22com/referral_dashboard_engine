from http import api_request
from http import dumps
from http import response_to_dict
from heymoose.utils.workers import app_logger
from xml_parser import xpath_to_string
from resource_order import order_to_dict
from resource_order import construct_orders_from_xml
from lxml import etree

import sys

resource_path = "/users"

def construct_user_from_xml(xml_string): # it is work:)) Maybe we should use json instead?
	if not xml_string:
		return None

	try:
		res = {}
		res['email'] = xpath_to_string(xml_string, '/user/email')
		res['name'] = xpath_to_string(xml_string, '/user/nickname')
		res['password'] = xpath_to_string(xml_string, '/user/password-hash')
		res['id'] = xpath_to_string(xml_string, '@id')
		
		# test if we are developers
		try:
			dev = {} # to have res always valid
			xpath_to_string(xml_string, '/user/app')
			dev['app_id'] = xpath_to_string(xml_string, '/user/app/@id')
			dev['secret_key'] = xpath_to_string(xml_string, '/user/app/secret')

			#if we come here all fields of developer are correct
			res.update(dev)
		except Exception as inst:
			app_logger.error(inst)
			app_logger.error(sys.exc_info())
			print "We can't become a valid developer"
		
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


def add_user(email, password, nickname):
	path = resource_path 
	data = dict(email=email, password=password, nickname=nickname)
	payload=dumps(data)

	app_logger.debug("add_user " + path)
	return api_request(path=path, payload=payload, type="POST")

def get_user_by_id(id):
	path = resource_path + "/" + str(id)	#TODO: make generic parameters build
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
