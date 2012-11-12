from backend import BackendResource, extractor
from heymoose.data.models import BlackListSite


class SiteResource(BackendResource):
	base_path = '/sites'
	extractor = extractor()

	def extract_blacklist_site_params(self, site):
		return self.extractor.extract(site, required=['host'], optional=['sub_domain_mask', 'path_mask', 'comment'])

	def blacklist_get(self, id):
		return self.path('blacklist').path(id).get().as_obj(BlackListSite)

	def blacklist_add(self, site):
		self.path('blacklist').post(**self.extract_blacklist_site_params(site))

	def blacklist_update(self, site):
		params = self.extractor.extract(site, required=['host'], optional=['subdomain_mask', 'path_mask', 'comment'])
		self.path('blacklist').path(site.id).put(**self.extract_blacklist_site_params(site))

	def blacklist_remove(self, id):
		self.path('blacklist').path(id).delete()

	def blacklist(self, **kwargs):
		return self.path('blacklist').get(**kwargs).as_objlist(BlackListSite, with_count=True)