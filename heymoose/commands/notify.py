# -*- coding: utf-8 -*-
from heymoose import app, app_init_mail
from heymoose.commands import manager
import pymongo

NOTIFICATION_TEMPLATE = u'''
	<p>У вас имеется {{ count }} непрочитанных уведомлений в системе HeyMoose!</p>
	<p>Вот некоторые из них:</p>
	<ul>
		{% for notification in notifications %}
		<li>{{ notification|safe }}</li>
		{% endfor %}
	</ul>
	<p>Посетите личный кабинет HeyMoose, чтобы прочитать остальные уведомления.</p>
'''

@manager.command
def notify():
	app_init_mail(app)
	from pymongo import Connection
	from jinja2 import Template
	from collections import defaultdict
	from datetime import datetime
	from heymoose import resource as rc
	from heymoose.utils.convert import datetime_format
	
	app.logger.info('Started at {0}'.format(datetime.now().strftime(datetime_format)))
	
	database = app.config.get('MONGOALCHEMY_DATABASE')
	connection = Connection()
	db = connection[database]
	notifications = db['Notification']
	
	unnotified_user_ids = set()
	unread_by_user = defaultdict(list)
	for n in notifications.find({'read': False}).sort('date', pymongo.DESCENDING):
		user_id = n.get('user_id')
		unread_by_user[user_id].append(n.get('body'))
		if not n.get('notified'): unnotified_user_ids.add(user_id)
	
	if not unnotified_user_ids:
		app.logger.info('Nothing to send.')
		return
	
	template = Template(NOTIFICATION_TEMPLATE)
	with app.mail.connect() as conn:
		for user_id, unread in unread_by_user.iteritems():
			if user_id in unnotified_user_ids:
				user = rc.users.get_by_id(user_id)
				conn.send_message(
					subject=u'У вас есть непрочитанные уведомления',
					recipients=[user.email],
					html=template.render(count=len(unread), notifications=unread[:5])
				)
				notifications.update({'user_id': user_id}, {'$set': {'notified': True}}, multi=True)
	
	app.logger.info('All done! {0} emails sent'.format(len(unnotified_user_ids)))
	app.logger.info('Finished at {0}'.format(datetime.now().strftime(datetime_format)))
