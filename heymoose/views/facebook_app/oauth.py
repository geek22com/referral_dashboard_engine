# -*- coding: utf-8 -*-
import hashlib
import random
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.thirdparty.facebook.actions import users
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.thirdparty.facebook.mongo.data import Performer
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.thirdparty.facebook.actions.oauth as oauth
from heymoose import config
from heymoose.thirdparty.facebook.actions.oauth import OAUTH_DIALOG_PATH
FACEBOOK_APP_URL = config.get('FACEBOOK_APP_URL')
SCOPE = config.get('FACEBOOK_AUTH_SCOPE')

def oauth_dialog_url():
	return oauth.get_oauth_dialog_url(redirect_url=url_for('oauth_request', _external=True),
			scope=SCOPE)

#Facebook Iframe bug
@frontend.route("/facebook_app/javascript_redirect", methods=["GET", "POST"])
def javascript_redirect():
	g.params['SERVICE_URL'] = config.get('FACEBOOK_SERVICE_URL')
	g.params['OAUTH_DIALOG_PATH'] = OAUTH_DIALOG_PATH
	g.params['client_id'] = config.get('APP_ID')
	g.params['redirect_url'] = url_for('oauth_request', _external=True)
	g.params['scope'] = SCOPE
	return render_template('./facebook_app/oauth_redirect.html', params=g.params)

#TODO: is it simplier to store TokenObject in session?
#Server-side flow implementation: http://developers.facebook.com/docs/authentication/
@frontend.route("/facebook_app/oauth_request/", methods=["GET"])
def oauth_request():
	if not request.args.get('code', '') or request.args.get('error', '') == 'access_denied':
		return redirect(oauth_dialog_url())

	token, expires = oauth.get_acces_token(redirect_url=url_for('oauth_request',
													_external=True),
                                                code=request.args.get('code'))
	if not token:
		app_logger.debug("oauth_request: can't get token")
		return redirect(oauth_dialog_url())

	facebook_user = users.get_user("me", token)

	performer = performers.get_performer(facebook_user.get(u'id'))
	if performer:
		performer.dirty = False
		performer.oauth_token = token
		performer.expires = str(oauth.expires_to_absolute_epoch(expires))
		performer.fullname = facebook_user.get(u'name','')
		performer.firstname = facebook_user.get(u'first_name','')
		performer.lastname = facebook_user.get(u'last_name','')
	else:
		performer = Performer(dirty = False,
						    oauth_token = token,
						    expires = str(oauth.expires_to_absolute_epoch(expires)),
						    user_id = facebook_user.get(u'id', ''),
					        fullname = facebook_user.get(u'name', ''),
						    firstname = facebook_user.get(u'first_name', ''),
						    lastname = facebook_user.get(u'last_name', ''))
	performer.save()
	session['performer_id'] = performer.user_id

	return redirect(FACEBOOK_APP_URL)
