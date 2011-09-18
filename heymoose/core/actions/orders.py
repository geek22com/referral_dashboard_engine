from heymoose.core.actions.mappers import order_from_xml
from heymoose.core.rest import post, put
from heymoose.utils.workers import app_logger

resource_path = "/orders"

def add_order(userId, title, body, balance, cpa):
	app_logger.debug()
	post(path=resource_path,
			params_dict=dict(userId=userId,
				title=title,
				body=body,
	            balance=balance,
				cpa=cpa))

def get_order(order_id):
	path = "%s/%d".format(resource_path, order_id)
	return order_from_xml(get(path=path))

def approve_order(order_id):
	app_logger.debug()
	path =  "%s/%d".format(resource_path, order_id)
	put(path=path)
