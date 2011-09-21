# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose.settings.debug_config import APP_ID, DEVELOPER_SECRET_KEY, APP_SECRET
import heymoose.thirdparty.facebook.actions.oauth as oauth
import heymoose.thirdparty.facebook.actions.base as base
import heymoose.thirdparty.facebook.actions.social_graph as social_graph
from heymoose.utils.decorators import oauth_only
import heymoose.forms.forms as forms

def get_signed_request():
	signed_request = request.form.get('signed_request', '').decode('utf8')
	if not signed_request:
		signed_request = session.get('signed_request', '')
	return signed_request

def save_signed_request(signed_request):
	session['signed_request'] = signed_request

@frontend.route('/facebook_app/', methods=['GET', 'POST'])
def facebook_app():
		signed_request = get_signed_request()
		if not oauth.validate_token(session.get('access_token', ''),
									session.get('expires', '')):
			oauth.invalidate_session(session)
			save_signed_request(signed_request)
			return redirect(url_for('oauth_request'))

		valid, data = base.decrypt_request(signed_request)
		if valid:
			session['facebook_app_id'] = APP_ID
			g.params['app_id'] = APP_ID # We need this to init facebook javascript SDK
			session['facebook_user_id'] = data.get(u'user_id')
		else:
			app_logger.debug("facebook_app request Bad Signed")
			abort(404)

		return render_template('./facebook_app/heymoose-facebook.html', params=g.params)


##################################### AJAX methods #################################################################
@frontend.route('/channel/', methods=['GET', 'POST'])
def channel():
		return render_template('facebook-channel.html', params=g.params)

#Let's call it route polymorphism :)
#f.e: you call /facebook_tmpl/gifts
#     if we don't have explicit route for it, then
#     /facebook_tmpl/<tmpl> will be called

@frontend.route('/facebook_tmpl/gifts', methods=['GET'])
@oauth_only
def facebook_gifts():
	app_logger.debug("facebook_gifts user_id={0} request={1}".format(g.facebook_user_id,
	                                                                 request.url))
	g.params['friends'] = social_graph.get_friends(g.facebook_user_id,
	                                               g.access_token)
	return render_template('./facebook_app/gifts.html', params=g.params)

@frontend.route('/facebook_tmpl/<tmpl>', methods=['GET', 'POST'])
def facebook_tmpl(tmpl):
		template = "./facebook_app/{0}.html".format(tmpl)
		return render_template(template, params=g.params)
