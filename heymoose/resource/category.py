from backend import BackendResource
from heymoose.data.models import Category, CategoryGroup


class CategoryResource(BackendResource):
	base_path = '/categories'
	
	def list(self):
		return self.get().as_objlist(Category)
	
	def list_groups(self):
		return self.path('groups').get().as_objlist(CategoryGroup)
	
	def add(self, name, group_id):
		self.post(name=name, category_group_id=group_id)

	def update(self, id, name, group_id):
		self.path(id).put(name=name, category_group_id=group_id)
	
	def remove(self, id):
		self.path(id).delete()
	
	def add_group(self, name):
		self.path('groups').post(name=name)
	
	def update_group(self, id, name):
		self.path('groups').path(id).put(name=name)
	
	def remove_group(self, id):
		self.path('groups').path(id).delete()