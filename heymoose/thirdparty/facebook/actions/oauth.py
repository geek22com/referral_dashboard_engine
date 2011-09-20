# -*- coding: utf-8 -*-
import urlparse
import urllib
from heymoose.core.rest import get
from heymoose.settings.debug_config import APP_ID, APP_SECRET, FACEBOOK_SERVICE_URL, FACEBOOK_GRAPH_URL


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
	access_token_obj = get(base=FACEBOOK_GRAPH_URL,
							path=OAUTH_TOKEN_PATH,
							params_dict=dict(client_id=APP_ID,
								redirect_uri=redirect_url,
								client_secret=APP_SECRET,
								code=code),
							renderer=urlparse.parse_qs)

	#TODO: handle access..['expires'] parameters
	return access_token_obj['access_token']
	


### TESTS START HERE ###
import unittest

class OauthTest(unittest.TestCase):
	def test_oauth_dialog(self):
		res = get_oauth_dialog_url("http://heymoose.com:8080/", 123, 'email')
		self.assertEqual(type(res), str)
		print res

if __name__ == "__main__":
	unittest.main()