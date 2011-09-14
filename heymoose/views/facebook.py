# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
#from heymoose.db.models import Developer
import heymoose.forms.forms as forms
import hashlib
import base64
import json
import hmac

def base64_url_decode(data):
	data = data.encode(u'ascii')
	data += '=' * (4 - (len(data) % 4))
	return base64.urlsafe_b64decode(data)

@frontend.route('/facebook_app/', methods=['GET', 'POST'])
def facebook_app():
	happ = {}
#	app_developer = Developer.get_vkontakte_app_developer()
#	if not app_developer:
#		abort(404)

#	happ['app_id'] = app_developer.app_id

#	secret = app_developer.secret_key
#	req_sig = hashlib.md5()
#	req_sig.update(str(happ['app_id']) + secret)

#	happ['sig'] = req_sig.hexdigest()
	#worked facebook signed_request
#	signed_request = request.form.get('signed_request', '0').decode('utf8')
#	if signed_request:
#		sig, payload  = signed_request.split(u'.', 1)
#		sig = base64_url_decode(sig)
#		data = json.loads(base64_url_decode(payload))
		
#		expected_sig = hmac.new('3ca1d75b952eeef29625ffc42df61ddf', msg=payload, digestmod=hashlib.sha256).digest()
#		if sig == expected_sig:
#			signed_request = data
#			user_id = data.get(u'user_id')
#			happ['user_id'] = user_id
#			app_logger.debug('Going to print user info')
#			app_logger.debug(user_id)
#		else:
#			app_logger.debug('Bad signed_request')
#	g.params['happ'] = happ
	return render_template('heymoose-facebook.html', params=g.params)

@frontend.route('/channel/', methods=['GET', 'POST'])
def channel():
	return render_template('facebook-channel.html', params=g.params)
