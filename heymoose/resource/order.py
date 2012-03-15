from backend import ModelResource

class OrderResource(ModelResource):
	model_name = 'Order'
	base_path = '/orders'
	
	def get_by_id(self, id, **kwargs):
		return self.model(self.path(id).get(**kwargs))