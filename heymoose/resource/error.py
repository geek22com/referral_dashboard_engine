from backend import BackendResource
from heymoose.data.models import ApiError


class ErrorResource(BackendResource):
	base_path = '/errors'
	
	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(ApiError, with_count=True)