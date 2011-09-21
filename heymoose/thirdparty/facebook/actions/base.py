# -*- coding: utf-8 -*-
from heymoose.settings.debug_config import APP_SECRET, DEVELOPER_SECRET_KEY
import hashlib
import base64
import json
import hmac
from heymoose.utils.workers import app_logger

def base64_url_decode(data):
		data = data.encode(u'ascii')
		data += '=' * (4 - (len(data) % 4))
		return base64.urlsafe_b64decode(data)

def decrypt_request(signed_request):
	if not signed_request:
		app_logger.debug("Can't decrypt signed_request={0}".format(signed_request))
		return (False, None)

	sig, payload  = signed_request.split(u'.', 1)
	sig = base64_url_decode(sig)
	data = json.loads(base64_url_decode(payload))

	expected_sig = hmac.new(APP_SECRET, msg=payload, digestmod=hashlib.sha256).digest()
	if sig != expected_sig:
		app_logger.debug("Sig != expected_sig")
		return (False, None)
	
	return (True, data)

def sign_parameter(param):
	req_sig = hashlib.md5()
	req_sig.update(str(param) + DEVELOPER_SECRET_KEY)
	return req_sig.hexdigest()
