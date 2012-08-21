# -*- coding: utf-8 -*-
from heymoose.db.models import Notification
from heymoose.data.enums import OfferGrantState, Roles
from heymoose import resource as rc
from flask import render_template_string
from datetime import datetime

def create_notification(id, text):
	Notification(user_id=id, body=text, date=datetime.now()).save()

def notify_all(text, **kwargs):
	users = rc.users.list(offset=0, limit=999999, **kwargs)
	for user in users:
		create_notification(user.id, text)

def notify_all_affiliates(text, **kwargs):
	notify_all(text, role=Roles.AFFILIATE, **kwargs)

def notify_all_advertisers(text, **kwargs):
	notify_all(text, role=Roles.ADVERTISER, **kwargs)

def notify_users(users, template, **kwargs):
	text = render_template_string(template, **kwargs)
	for user in users:
		create_notification(user.id, text)

def notify_user(user, template, **kwargs):
	notify_users([user], template, **kwargs)

def notify_admin(template, **kwargs):
	text = render_template_string(template, **kwargs)
	create_notification(0, text)

def notify_offer_affiliates(offer, template, **kwargs):
	grants, _ = rc.offer_grants.list(offer_id=offer.id,
		state=OfferGrantState.APPROVED, blocked=False, offset=0, limit=999999)
	affiliates = [grant.affiliate for grant in grants]
	notify_users(affiliates, template, offer=offer, **kwargs)