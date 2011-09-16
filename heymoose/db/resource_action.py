from http import api_request
from lxml import etree
from http import dumps
from http import response_to_dict
from heymoose.utils.workers import app_logger
from xml_parser import xpath_to_string
import sys

# Using new REST API
resource_path = "/actions"

def action_to_dict(action_element):
	item = {}
	try:
		item['id'] = str(action_element.xpath("@id")[0])
		item['performer_id'] = action_element.xpath("performer-id")[0].text.decode('utf8')
		item['offer_id'] = action_element.xpath("offer-id")[0].text.decode('utf8')
		item['done'] = action_element.xpath("done")[0].text.decode('utf8')
		item['deleted'] = action_element.xpath("deleted")[0].text.decode('utf8')
		item['creation_time'] = action_element.xpath("creation-time")[0].text.decode('utf8')
		return item
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def construct_actions_from_xml(xml_string):
	if not xml_string:
		return None
	try:
		res = []
		root = etree.fromstring(xml_string)
		actions = root.find('actions')

		for action in actions:
			item = action_to_dict(action)
			if item:
				res.append(item)
		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def get_actions(offset, limit):
	path = resource_path
	response = api_request(path=path)

	app_logger.debug("get_actions " + path)
	return response_to_dict(response, func=construct_actions_from_xml)

def approve_action(action_id):
	path = resource_path + "/" + str(action_id)

	app_logger.debug("confirm_action " + path)
	return api_request(path=path, type="PUT")

def delete_action(action_id):
	path = resource_path + "/" + str(action_id)

	app_logger.debug("delete_action " + path)
	return api_request(path=path, type="DELETE")