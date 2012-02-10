from heymoose.core.actions.mappers import user_from_xml, withdrawal_from_xml, count_from_xml
from heymoose.core.rest import get, put, post, delete
from heymoose.core.actions import roles
from heymoose.utils import shortcuts, convert
from restkit.errors import ResourceNotFound

resource_path = "/users"

def add_user_role(user_id, role):
	path = "{0}/{1}/roles".format(resource_path, user_id)
	post(path=path, params_dict=dict(role=role))

def become_developer(user_id):
	return add_user_role(user_id, roles.DEVELOPER)

def become_customer(user_id):
	return add_user_role(user_id, roles.CUSTOMER)

def add_user(email, password_hash, first_name, last_name, organization=None, phone=None, 
			source_url=None, messenger_type=None, messenger_uid=None, referrer_id=None):
	params = dict(email=email, passwordHash=password_hash, firstName=first_name, lastName=last_name)
	shortcuts.dict_update_filled_params(params, organization=organization, phone=phone,
		sourceUrl=source_url, messengerType=messenger_type, messengerUid=messenger_uid,
		referrer=referrer_id)
	post(path=resource_path, params_dict=params)
	
def update_user(user_id, **kwargs):
	path = "{0}/{1}".format(resource_path, user_id)
	params = dict([(convert.to_camel_case(k), v) for k, v in kwargs.iteritems()])
	put(path=path, params_dict=params)
	
def confirm_user(user_id):
	path = "{0}/{1}/confirmed".format(resource_path, user_id)
	put(path=path)
	
def block_user(user_id):
	path = "{0}/{1}/blocked".format(resource_path, user_id)
	put(path=path)
	
def unblock_user(user_id):
	path = "{0}/{1}/blocked".format(resource_path, user_id)
	delete(path=path)
	
def change_user_email(user_id, email):
	path = "{0}/{1}/email".format(resource_path, user_id)
	put(path=path, params_dict=dict(email=email))

def get_user_by_id(id, **kwargs):
	path = "{0}/{1}".format(resource_path, id)
	return user_from_xml(get(path=path, params_dict=kwargs))

def get_user_by_email(email, **kwargs):
	try:
		kwargs.update(dict(email=email))
		return user_from_xml(get(path=resource_path, params_dict=kwargs))
	except ResourceNotFound:
		return None
	
def get_users(**kwargs):
	path = "{0}/{1}".format(resource_path, 'list')
	return map(user_from_xml, get(path=path, params_dict=kwargs))

def get_users_count(**kwargs):
	path = "{0}/{1}/{2}".format(resource_path, 'list', 'count')
	return count_from_xml(get(path=path, params_dict=kwargs))
	
def increase_customer_balance(user_id, amount):
	path =  "{0}/{1}/customer-account".format(resource_path, user_id)
	put(path=path, params_dict=dict(amount=amount))


def get_user_withdrawals(user_id):
	path = "{0}/{1}/developer-account/withdraws".format(resource_path, user_id)
	return map(withdrawal_from_xml, get(path=path))

def make_user_withdrawal(user_id, amount):
	path = "{0}/{1}/developer-account/withdraws".format(resource_path, user_id)
	return post(path=path, params_dict=dict(amount=amount))

def approve_user_withdrawal(user_id, withdrawal_id):
	path = "{0}/{1}/developer-account/withdraws/{2}".format(resource_path, user_id, withdrawal_id)
	return put(path=path)

def delete_user_withdrawal(user_id, withdrawal_id, comment):
	path = "{0}/{1}/developer-account/withdraws/{2}".format(resource_path, user_id, withdrawal_id)
	return delete(path=path, params_dict=dict(comment=comment))
