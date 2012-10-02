# -*- coding: utf-8 -*-
from flask import g, request, redirect
from heymoose import app
from heymoose.cabinetcpa import blueprint as bp
from heymoose.data.mongo.models import Notification
from heymoose.views.decorators import template, paginated

NOTIFICATIONS_PER_PAGE = app.config.get('NOTIFICATIONS_PER_PAGE', 10)

@bp.route('/notifications/', methods=['GET', 'POST'])
@template('cabinetcpa/notifications.html')
@paginated(NOTIFICATIONS_PER_PAGE)
def notifications(offset, limit, **kwargs):
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