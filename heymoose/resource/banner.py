from backend import BackendResource
from heymoose.data.models import Banner


class BannerResource(BackendResource):
	base_path = '/banners'

	def list(self, offer_id, **kwargs):
		return self.get(offer_id=offer_id, **kwargs).as_objlist(Banner, with_count=True)

	def remove_by_ids(self, offer_id, banner_ids):
		self.delete(offer_id=offer_id, banner_ids=banner_ids)