# -*- coding: utf-8 -*-
import json
from restkit.errors import RequestFailed
from flask import Flask, request, session, url_for, redirect, \
	 render_template, abort, g, flash
from heymoose.thirdparty.facebook.actions import base
from heymoose.thirdparty.facebook.mongo import performers
from heymoose.thirdparty.facebook.mongo.performers import create_action_offer, create_action_mlm
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose import config
import heymoose.forms.forms as forms
from heymoose.thirdparty.facebook.mongo.data import AccountAction
from datetime import datetime

def offer_callback(form):
	extId = form.get('extId').decode('utf8')
	offerId = form.get('offerId').decode('utf8')
	amount = int(form.get('amount').decode('utf8'))
	create_action_offer(extId, offerId, amount)
	app_logger.debug("offer_callback for extId={0} offerId={1} amount={2}".format(extId, offerId, amount))

def mlm_callback(form):
	appId = form.get('appId').decode('utf8')
	fromTime = form.get('fromTime').decode('utf8')
	toTime = form.get('toTime').decode('utf8')
	items = json.loads(form.get('items').decode('utf8'))
	app_logger.debug("mlm callback called for appId={0} fromTime={1} toTime={2} items={3}".format(appId, fromTime, toTime, str(items)))
	
	for item in items:
		if not create_action_mlm(item[u'extId'], int(item[u'passiveRevenue'])):
			app_logger.debug("Error try to calc negative revenue appId={0} fromTime={1} toTime={2}".format(appId, fromTime, toTime))


@frontend.route('/main_callback/', methods=['POST'])
def main_callback():
	app_logger.debug("main_callback form:{0}".format(request.form))
	try:
		if request.form.get('items', ''):
			mlm_callback(request.form)
		else:
			offer_callback(request.form)
	except Exception as inst:
		app_logger.debug("{0} main_callback shit happened exception={1}".format(datetime.now(), inst))
		raise
	return "Ok"