from backend import BackendResource
from heymoose.data.models import Category


class CategoryResource(BackendResource):
	base_path = '/categories'
	
	def list(self):
		return self.get().as_objlist(Category)