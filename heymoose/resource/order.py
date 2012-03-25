from backend import BackendResource
from heymoose.data.models import Order

class OrderResource(BackendResource):
	base_path = '/orders'
	
	def get_by_id(self, id, **kwargs):
		return Order(self.path(id).get(**kwargs))