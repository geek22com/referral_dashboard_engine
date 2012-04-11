from heymoose import app
from mailjet import api
import transactional

users_list_id = app.config.get('MAILJET_USERS_LIST_ID')
advertisers_list_id = app.config.get('MAILJET_ADVERTISERS_LIST_ID')
affiliates_list_id = app.config.get('MAILJET_AFFILIATES_LIST_ID')

def lists_add_user(user, mail_if_failed=True):
	try:
		api.lists_add_contact(user.email, users_list_id, True)
		if user.is_advertiser:
			api.lists_add_contact(user.email, advertisers_list_id, True)
		if user.is_affiliate:
			api.lists_add_contact(user.email, affiliates_list_id, True)
		return True
	except:
		app.logger.error(u'Failed to add user {0} ({1}) to one or multiple mailing lists'
			.format(user.full_name(), user.email), exc_info=True)
		if mail_if_failed: transactional.admin_list_add_failed(user)
		return False