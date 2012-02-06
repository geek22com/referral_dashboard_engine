from heymoose import app
from mailjet import api
import transactional

users_list_id = app.config.get('MAILJET_USERS_LIST_ID')
customers_list_id = app.config.get('MAILJET_CUSTOMERS_LIST_ID')
developers_list_id = app.config.get('MAILJET_DEVELOPERS_LIST_ID')

def lists_add_user(user):
	try:
		api.lists_add_contact(user.email, users_list_id, True)
		if user.is_customer():
			api.lists_add_contact(user.email, customers_list_id, True)
		if user.is_developer():
			api.lists_add_contact(user.email, developers_list_id, True)
	except:
		app.logger.error(u'Failed to add user {0} ({1}) to one or multiple mailing lists'
			.format(user.full_name(), user.email), exc_info=True)
		transactional.admin_list_add_failed(user)