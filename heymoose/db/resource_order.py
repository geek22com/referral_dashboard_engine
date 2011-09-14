from http import api_request
from lxml import etree
from http import dumps
from http import response_to_dict
from heymoose.utils.workers import app_logger
from xml_parser import xpath_to_string
import sys

# Using new REST API
resource_path = "/orders"

def order_to_dict(order_element, user_id):
	item = {}
	try:
		item['id'] = str(order_element.xpath("@id")[0])
		item['title'] = order_element.xpath("title")[0].text.decode('utf8')
		item['balance'] = order_element.xpath("balance")[0].text.decode('utf8')
		item['user_id'] = user_id
		item['body'] = ''
		item['cpa'] = 12
		return item
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def construct_order_from_xml(xml_string):
	if not xml_string:
		return None
	
	res = {}
	try:
		res['id'] = xpath_to_string(xml_string, '@id')
		res['title'] = xpath_to_string(xml_string, '/order/title')
		res['balance'] = xpath_to_string(xml_string, '/order/balance')
		res['user_id'] = xpath_to_string(xml_string, '/order/user-id')
		res['body'] = ''
		res['cpa'] = 12
		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def construct_orders_from_xml(xml_string):
	if not xml_string:
		return None
	try:
		res = []
		root = etree.fromstring(xml_string)
		orders = root.find('orders')
		user_id = xpath_to_string(xml_string, '@id')
		
		for order in orders:
			item = order_to_dict(order, user_id)
			if item:
				res.append(item)
		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def add_order(userId, title, body, balance, cpa):
	path = resource_path
	data = dict(userId=userId, 
			title=title,
			body=body,
	        balance=balance,
			cpa=cpa)
	payload=dumps(data)
	app_logger.debug("add_order " + path)
	return api_request(path=path, payload=payload, type="POST")

def get_order(order_id):
	path = resource_path + "/" + str(order_id) #TODO: make generic parameters build
	response = api_request(path=path)

	app_logger.debug("load_order " + path)
	return response_to_dict(response, func=construct_order_from_xml)
