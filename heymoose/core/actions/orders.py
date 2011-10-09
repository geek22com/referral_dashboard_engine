from heymoose.core.actions.mappers import order_from_xml
from heymoose.core.rest import post, put, get
from heymoose.utils.workers import app_logger
from restkit.errors import RequestFailed

resource_path = "/orders"

def add_order(userId, title, body, balance, cpa, desc, image_data):
	try:
		post(path=resource_path,
			params_dict=dict(userId=userId,
				title=title,
				body=body,
	            balance=balance,
				cpa=cpa,
				description=desc,
				image=image_data,
				autoAprove="true"))
	except RequestFailed:
		return False
	return True

def get_order(order_id):
	path = "{0}/{1}".format(resource_path, order_id)
	return order_from_xml(get(path=path))

def approve_order(order_id):
	path =  "{0}/{1}".format(resource_path, order_id)
	put(path=path)

def get_orders(offset, limit):
	return map(order_from_xml, get(path=resource_path,
									params_dict=dict(offset=offset,
									limit=limit)))
