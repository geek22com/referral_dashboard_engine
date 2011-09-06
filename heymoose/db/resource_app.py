from http import api_request
from http import dumps
from heymoose.utils.workers import app_logger
import sys

resource_path = "/apps"

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


def become_developer(userid, platform):
	path = resource_path
	data = dict(userId=userid, platform=platform)
	payload=dumps(data)

	app_logger.debug("become_developer " + path)
	return api_request(path=path, payload=payload, type="POST")

def get_app(app_id):
	path = resource_path + "/" + str(app_id)
	response = api_request(path=path)

	app_logger.debug("get_app" + path)
	return response_to_dict(response, func=construct_app_from_xml)

