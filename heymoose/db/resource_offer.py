from http import api_request
from http import dumps
from heymoose.utils.workers import app_logger
from xml_parser import xpath_to_string
import sys

resource_path = "/offers"

def get_offers(app_id, secret):
	path = resource_path
	params = {'app' : app_id, 'secret' : secret}
	response = api_request(path=path, params_dict=params)

	app_logger.debug("get_offers " + path)
	#return response_to_dict(response, func=construct_order_from_xml)
	return response
