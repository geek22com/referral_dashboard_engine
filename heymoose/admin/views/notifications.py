# -*- coding: utf-8 -*-
from flask import request, redirect, flash, url_for, g
from heymoose import app
from heymoose.admin import blueprint as bp
from heymoose.db.models import Notification
from heymoose.forms import forms
from heymoose.notifications.base import notify_all, notify_all_affiliates, notify_all_advertisers
from heymoose.views.decorators import template, paginated

NOTIFICATIONS_PER_PAGE = app.config.get('NOTIFICATIONS_PER_PAGE', 10)

@bp.route('/notifications/', methods=['GET', 'POST'])
@template('admin/notifications/list.html')
@paginated(NOTIFICATIONS_PER_PAGE)
def notifications_list(offset, limit, **kwargs):
	user_notifications_query = Notification.query.filter(Notification.user_id == g.user.id)
	if request.method == 'POST':
		if 'all' in request.form:
			notifications = user_notifications_query.filter(Notification.read == False)
		else:
			ids = request.form.getlist('id')
			notifications = user_notifications_query.filter(Notification.mongo_id.in_(*ids))
		notifications.set(read=True, notified=True).multi().execute()
		return redirect(request.url)
	notifications = user_notifications_query.descending(Notification.date).skip(offset).limit(limit).all()
	count = user_notifications_query.count()
	return dict(notifications=notifications, count=count)

@bp.route('/notifications/new/', methods=['GET', 'POST'])
@template('admin/notifications/new.html')
def notifications_new():
	form = forms.NotificationForm(request.form)
	if request.method == 'POST' and form.validate():
		if form.role.data == 0: notify_all(form.text.data)
		elif form.role.data == 1: notify_all_affiliates(form.text.data)
		elif form.role.data == 2: notify_all_advertisers(form.text.data)			
		flash(u'Уведомление успешно отправлено', 'success')
		return redirect(url_for('.notifications_list'))
	return dict(form=form)