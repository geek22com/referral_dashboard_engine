from backend import BackendResource
from heymoose.data.models import Region


class RegionResource(BackendResource):
	base_path = '/regions'
	
	def list(self):
		return self.get().as_objlist(Region)