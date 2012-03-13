from heymoose.data.models import User
from backend import BackendResource
from utils.path import path


class UserResource(BackendResource):
	path = '/users'
	
	def get_by_id(self, id, **kwargs):
		return User(self.get(path(id).build(), **kwargs))
	
	def add_role(self, id, role):
		return self.post(path(id).path('roles').build(), role=role)
	
	def create(self):
		pass