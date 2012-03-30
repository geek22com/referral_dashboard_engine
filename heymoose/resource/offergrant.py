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
	
	def list_offers(self, **kwargs):
		grants, count = self.list(**kwargs)
		offers = []
		for grant in grants:
			offer = grant.offer
			offer.grant = grant
			offers.append(offer)
		return offers, count
	
	def add(self, offer_grant, **kwargs):
		params = self.extractor.extract(offer_grant, required='offer_id aff_id message'.split())
		params.update(kwargs)
		return self.post(**params).as_int()
	
	def activate(self, id):
		self.path(id).path('active').put()
	
	def approve(self, id):
		self.path(id).path('approved').put()