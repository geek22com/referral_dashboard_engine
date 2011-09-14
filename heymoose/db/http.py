from heymoose.utils.workers import app_logger
from restkit import request
from restkit import Resource
import heymoose.settings.debug_config as config
import sys

url_base = config.RESTAPI_SERVER

def api_request(path, payload=None, params_dict=None, type='GET'):
	try:
		response = None
		res = Resource(url_base)
		if type == 'GET':
		   response = res.get(path=path, params_dict=params_dict) # add timeout here
		elif type == 'PUT':
			response = res.put(path=path, payload=payload)
		elif type == 'POST':
			response = res.post(path=path, payload=payload)
		else:
			raise Exception('Unknown request type')

		return response
	except Exception as inst: # We don't need to test response code. We always got exception if not 20* ??
		app_logger.error(inst)
		app_logger.error(sys.exc_info())
		if getattr(inst, 'response', False):
			app_logger.error(inst.response.final_url)
		return None



def dumps(dct): # make it easy. map.. (I need handbook to remember all this stuff, so not now man:)))
	data = ""
	for k,v in dct.items():
		data += str(k) + "=" + str(v) + '&'
	data = data.strip('&')
	return data

def response_to_dict(response, func):
	if response and response.can_read():
		return func(response.body_string())
	else:
		return None
