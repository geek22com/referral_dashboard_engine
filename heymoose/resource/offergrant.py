from backend import BackendResource, extractor
from heymoose.data.models import OfferGrant


class OfferGrantResource(BackendResource):
	base_path = '/grants'
	
	extractor = extractor().alias(
		offer_id='offer.id',
		aff_id='affiliate.id'
	)
	
	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(OfferGrant)
	
	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(OfferGrant, with_count=True)
	
	def add(self, offer_grant, **kwargs):
		params = self.extractor.extract(offer_grant, required='offer_id aff_id message'.split())
		params.update(kwargs)
		return self.post(**params).as_int()