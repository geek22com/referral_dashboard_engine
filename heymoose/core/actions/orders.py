from heymoose.core.actions.mappers import order_from_xml, count_from_xml
from heymoose.core.rest import post, put, get
from heymoose.utils.workers import app_logger
from restkit.errors import RequestFailed

resource_path = "/orders"

# Adds a new order. Possible kwargs: male (bool), minAge (int), maxAge (int).
def add_order(userId, title, body, balance, cpa, desc, image_data, autoApprove=True, 
			allowNegativeBalance=True, **kwargs):
	try:
		post(path=resource_path,
			params_dict=dict(userId=userId,
				title=title,
				body=body,
	            balance=balance,
				cpa=cpa,
				description=desc,
				image=image_data,
				autoApprove=autoApprove,
				allowNegativeBalance=allowNegativeBalance,
				**kwargs))
	except RequestFailed:
		return False
	return True

def get_order(order_id, **kwargs):
	path = "{0}/{1}".format(resource_path, order_id)
	return order_from_xml(get(path=path, params_dict=kwargs))

def approve_order(order_id):
	path =  "{0}/{1}".format(resource_path, order_id)
	put(path=path)

def get_orders(**kwargs):
	return map(order_from_xml, get(path=resource_path, params_dict=kwargs))

def get_orders_count():
	path = "{0}/{1}".format(resource_path, "count")
	return count_from_xml(get(path=path))
