from backend import BackendResource, extractor
from heymoose.data.models import Site, BlackListSite, SiteStat


class SiteResource(BackendResource):
	base_path = '/sites'
	extractor = extractor().alias(aff_id='affiliate.id')

	def extract_site_params(self, site):
		return self.extractor.extract(site,
			required='aff_id type name description'.split(),
			optional='url stats_url stats_description hosts_count members_count context_system'.split())

	def extract_site_moderation_params(self, site):
		return self.extractor.extract(site, required=['admin_state'], optional=['admin_comment'])

	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(Site)

	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(Site, with_count=True)

	def add(self, site):
		self.post(**self.extract_site_params(site))

	def update(self, site):
		self.path(site.id).put(**self.extract_site_params(site))

	def moderate(self, site):
		self.path(site.id).path('moderate').put(**self.extract_site_moderation_params(site))

	def extract_blacklist_site_params(self, site):
		return self.extractor.extract(site, required=['host'], optional=['sub_domain_mask', 'path_mask', 'comment'])

	def blacklist_get(self, id):
		return self.path('blacklist').path(id).get().as_obj(BlackListSite)

	def blacklist_add(self, site):
		self.path('blacklist').post(**self.extract_blacklist_site_params(site))

	def blacklist_update(self, site):
		self.path('blacklist').path(site.id).put(**self.extract_blacklist_site_params(site))

	def blacklist_remove(self, id):
		self.path('blacklist').path(id).delete()

	def blacklist(self, **kwargs):
		return self.path('blacklist').get(**kwargs).as_objlist(BlackListSite, with_count=True)

	def list_stats(self, **kwargs):
		return self.path('stats').get(**kwargs).as_objlist(SiteStat, with_count=True)