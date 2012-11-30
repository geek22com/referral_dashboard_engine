from backend import BackendResource, extractor
from heymoose.data.models import Placement


class PlacementResource(BackendResource):
	base_path = '/placements'
	extractor = extractor().alias(site_id='site.id', offer_id='offer.id')

	def extract_placement_params(self, placement):
		return self.extractor.extract(placement,
			required='site_id offer_id'.split(),
			optional='back_url postback_url'.split())

	def extract_placement_moderation_params(self, placement):
		return self.extractor.extract(placement, required=['admin_state'], optional=['admin_comment'])

	def get_by_id(self, placement_id, **kwargs):
		return self.path(placement_id).get(**kwargs).as_obj(Placement)

	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(Placement, with_count=True)

	def add(self, placement):
		self.post(**self.extract_placement_params(placement))

	def update(self, placement):
		self.path(placement.id).put(**self.extract_placement_params(placement))

	def remove(self, placement):
		self.path(placement.id).delete()

	def moderate(self, placement):
		self.path(placement.id).path('moderate').put(**self.extract_placement_moderation_params(placement))