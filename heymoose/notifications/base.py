# -*- coding: utf-8 -*-
from heymoose.data.enums import Roles
from heymoose.data.mongo.models import Notification
from heymoose import resource as rc
from flask import render_template_string
from datetime import datetime

def create_notification(id, text, notified=False):
	Notification(user_id=id, body=text, date=datetime.now(), notified=notified).save()

def notify_all(text, **kwargs):
	users = rc.users.list(offset=0, limit=999999, **kwargs)
	for user in users:
		create_notification(user.id, text)

def notify_all_affiliates(text, **kwargs):
	notify_all(text, role=Roles.AFFILIATE, **kwargs)

def notify_all_advertisers(text, **kwargs):
	notify_all(text, role=Roles.ADVERTISER, **kwargs)

def notify_users(users, template, notified=False, **kwargs):
	text = render_template_string(template, **kwargs)
	for user in users:
		create_notification(user.id, text, notified=notified)

def notify_user(user, template, notified=False, **kwargs):
	notify_users([user], template, notified=notified, **kwargs)

def notify_admin(template, **kwargs):
	text = render_template_string(template, **kwargs)
	create_notification(0, text)
