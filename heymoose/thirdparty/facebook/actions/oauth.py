# -*- coding: utf-8 -*-
import urlparse
import urllib
import time
from restkit import RequestFailed
from heymoose.core.rest import get
from heymoose.settings.debug_config import APP_ID, APP_SECRET, FACEBOOK_SERVICE_URL, FACEBOOK_GRAPH_URL
import heymoose.thirdparty.facebook.actions.mappers as mappers
from heymoose.utils.workers import app_logger

OAUTH_DIALOG_PATH = "/dialog/oauth"
OAUTH_TOKEN_PATH = "/oauth/access_token"

#TODO: ADD CSRF protection
def get_oauth_dialog_url(redirect_url, csrf_protect, scope=None):
	params = dict(client_id=APP_ID,
					redirect_uri=redirect_url,
					state=csrf_protect)
	if scope:
		params['scope'] = scope

	params_encoded = urllib.urlencode(params)
	
	return "{0}{1}?{2}".format(FACEBOOK_SERVICE_URL, OAUTH_DIALOG_PATH, params_encoded)

def get_acces_token(redirect_url, code):
	try:
		access_token_obj = get(base=FACEBOOK_GRAPH_URL,
							path=OAUTH_TOKEN_PATH,
							params_dict=dict(client_id=APP_ID,
								redirect_uri=redirect_url,
								client_secret=APP_SECRET,
								code=code),
							renderer=urlparse.parse_qs)
	except RequestFailed:
		return (None, None)

	#TODO: handle access..['expires'] parameters
	return (mappers.token_from_obj(access_token_obj),
			mappers.expires_from_obj(access_token_obj))
	
def validate_token(access_token, expires):
	if not access_token or not expires:
		app_logger.debug("Invalid token token={0} expires={1}".format(access_token, expires))
		return False

	if time.time() >= float(expires):
		app_logger.debug("Token time expired expires={0} current={1}".format(expires, time.time()))
		return False

	return True

def invalidate_session(session_obj):
	session_obj.pop('access_token', None)
	session_obj.pop('expires', None)
	session_obj.pop('state', None)

def expires_to_absolute_epoch(sec):
	return time.time() + float(sec)

### TESTS START HERE ###
import unittest

class OauthTest(unittest.TestCase):
	def test_oauth_dialog(self):
		res = get_oauth_dialog_url("http://heymoose.com:8080/", 123, 'email')
		self.assertEqual(type(res), str)
		print res

if __name__ == "__main__":
	unittest.main()