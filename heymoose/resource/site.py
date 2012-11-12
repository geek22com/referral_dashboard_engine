from backend import BackendResource, extractor
from heymoose.data.models import BlackListSite


class SiteResource(BackendResource):
	base_path = '/sites'
	extractor = extractor()

	def get_by_id(self, id):
		return self.path(id).get().as_obj(BlackListSite)

	def add(self, site):
		params = extractor.extract(site, required=['host'], optional=['subdomain_mask', 'path_mask'])
		return self.post(**params)

	def remove(self, id):
		self.path(id).delete()
