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

@frontend.route('/offer_callback/', methods=['POST'])
def offer_callback():
	extId = request.form.get('extId').decode('utf8')
	offerId = request.form.get('offerId').decode('utf8')
	amount = request.form.get('amount').decode('utf8')
	create_action_offer(extId, offerId, amount)
	app_logger.debug("offer_callback for extId={0} offerId={1} amount={2}".format(extId, offerId, amount))

@frontend.route('/mlm_callback/', methods=['POST'])
def mlm_callback(data):
	appId = request.form.get('appId').decode('utf8')
	fromTime = request.form.get('fromTime').decode('utf8')
	toTime = request.form.get('toTime').decode('utf8')
	items = json.loads(request.form.get('items').decode('utf8'))
	app_logger.debug("mlm callback called for appId={0} fromTime={1} toTime={2} items={3}".format(appId, fromTime, toTime, str(items)))
	
	for item in items:
		if not create_action_mlm(item[u'extId'], item[u'passiveRevenue']):
			app_logger.debug("Error try to calc negative revenue appId={0} fromTime={1} toTime={2}".format(appId, fromTime, toTime))
