from heymoose.utils.workers import app_logger
from heymoose.core.actions.mappers import user_from_xml
from heymoose.core.rest import get, put, post
from heymoose.core.actions import roles

resource_path = "/users"

def add_user_role(user_id, role):
	app_logger.debug("params: user_id=%d role=%s".format(user_id, role))
	path = "%s/%d".format(resource_path, user_id)
	put(path=path,
	    params_dict=dict(role=role))

def become_developer(user_id):
	return add_user_role(user_id,
	                     roles.DEVELOPER)

def become_customer(user_id):
	return add_user_role(user_id,
	                     roles.CUSTOMER)

def add_user(email, password, nickname):
	app_logger.debug()
	post(path=resource_path,
	     params_dict=dict(email=email,
	                      passwordHash=password,
	                      nickname=nickname))

def get_user_by_id(id, full=True):
	app_logger.debug()
	path = "%s/%d".format(resource_path, id)
	return user_from_xml(get(path=path,
	                         params_dict=dict(full=full)))

def get_user_by_email(email, full=False):
	app_logger.debug()
	return user_from_xml(get(path=resource_path,
								params_dict=dict(email=email,
								                 full=full)))

def increase_customer_balance(user_id, amount):
	app_logger.debug()
	path =  "%s/%d/customer-account".format(resource_path, user_id)
	put(path=path,
		params_dict=dict(amount=amount))
