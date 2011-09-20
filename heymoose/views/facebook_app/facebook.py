# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose.settings.debug_config import APP_ID, DEVELOPER_SECRET_KEY, APP_SECRET
import heymoose.forms.forms as forms
import hashlib
import base64
import json
import hmac

def base64_url_decode(data):
		data = data.encode(u'ascii')
		data += '=' * (4 - (len(data) % 4))
		return base64.urlsafe_b64decode(data)

@frontend.route('/facebook_tmpl/<tmpl>', methods=['GET', 'POST'])
def facebook_tmpl(tmpl):
		template = "./facebook_app/{0}.html".format(tmpl)
		return render_template(template, params=g.params)

@frontend.route('/facebook_app/', methods=['GET', 'POST'])
def facebook_app():
		#TODO: make access_token expire test here
		if not session['access_token']:
			return redirect(url_for('oauth_request'))
		
		g.params['app_id'] = APP_ID

		secret = DEVELOPER_SECRET_KEY
		req_sig = hashlib.md5()
		req_sig.update(str(g.params['app_id']) + secret)

		g.params['sig'] = req_sig.hexdigest()
		#worked facebook signed_request
		signed_request = request.form.get('signed_request', '0').decode('utf8')
		if signed_request:
				sig, payload  = signed_request.split(u'.', 1)
				sig = base64_url_decode(sig)
				data = json.loads(base64_url_decode(payload))

				expected_sig = hmac.new(APP_SECRET, msg=payload, digestmod=hashlib.sha256).digest()
				if sig == expected_sig:
						signed_request = data
						user_id = data.get(u'user_id')
						g.params['user_id'] = user_id
						app_logger.debug('Going to print user info')
						app_logger.debug(user_id)
				else:
						app_logger.debug('Bad signed_request')
		return render_template('./facebook_app/heymoose-facebook.html', params=g.params)

@frontend.route('/channel/', methods=['GET', 'POST'])
def channel():
		return render_template('facebook-channel.html', params=g.params)
