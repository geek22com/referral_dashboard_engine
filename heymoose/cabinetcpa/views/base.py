# -*- coding: utf-8 -*-
from flask import g, abort
from heymoose import resource as rc
from heymoose.cabinetcpa import blueprint as bp
from heymoose.forms import forms
from heymoose.views.decorators import template
from heymoose.db.models import Notification


@template('cabinetcpa/index-affiliate.html')
def index_affiliate():
	form = forms.DateTimeRangeForm()
	args = dict(offset=0, limit=5, order='CONFIRMED_REVENUE', direction='DESC', **form.backend_args())
	stats, _ = rc.offer_stats.list_user(g.user, **args)
	
	user_notifications_query = Notification.query.filter(Notification.user_id == g.user.id)
	notifications = user_notifications_query.descending(Notification.date).limit(5).all()
	
	return dict(stats=stats, notifications=notifications)

@template('cabinetcpa/index-advertiser.html')
def index_advertiser():
	return dict()

@bp.route('/')
def index():
	if g.user.is_advertiser:
		return index_advertiser()
	elif g.user.is_affiliate:
		return index_affiliate()
	else:
		abort(403)
	
	



