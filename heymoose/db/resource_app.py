from http import api_request
from http import dumps
from heymoose.utils.workers import app_logger
from xml_parser import xpath_to_string
import sys

resource_path = "/apps"

def construct_apps_from_xml(xml_string):
	if not xml_string:
		return None

	res = []
	try:
		item = {}
		item['id'] = xpath_to_string(xml_string, '/app/@id')
		item['secret'] = xpath_to_string(xml_string, '/app/secret')
		item['user_id'] = xpath_to_string(xml_string, '@id')

		res.append(item)
		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None


def construct_app_from_xml(xml_string):
	if not xml_string:
		return None

	res = {}
	try:
		res['id'] = xpath_to_string(xml_string, '@id')
		res['secret'] = xpath_to_string(xml_string, '/app/secret')
		res['user_id'] = xpath_to_string(xml_string, '/app/user-id')
		return res
	except Exception as inst:
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		return None

def add_app(user_id):
	path = resource_path
	data = dict(userId=user_id)
	payload=dumps(data)

	app_logger.debug("add_app " + path)
	return api_request(path=path, payload=payload, type="POST")

def get_app(app_id):
	path = resource_path + "/" + str(app_id)
	response = api_request(path=path)

	app_logger.debug("get_app" + path)
	return response_to_dict(response, func=construct_app_from_xml)

def regenerate_secret(app_id):
	path = resource_path + "/" + str(app_id)
	response = api_request(path=path, type="PUT")

	app_logger.debug("regenerate_secret" + path)
	return response
