from backend import BackendResource, extractor
from heymoose.data.models import Offer, SubOffer


class OfferResource(BackendResource):
	base_path = '/offers'
	
	extractor = extractor().alias(
		advertiser_id='advertiser.id',
		cost='value'
	)
	
	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(Offer)
	
	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(Offer, with_count=True)
	
	def add(self, offer, balance, **kwargs):
		params = self.extractor.extract(offer,
			required='advertiser_id pay_method cost name description url title'.split(),
			nonempty='regions'.split(),
			optional='cpa_policy allow_negative_balance auto_approve reentrant logo_filename'.split()
		)
		params.update(balance=balance)
		params.update(kwargs)
		return self.post(**params).as_int()
	
	def list_suboffers(self, id, **kwargs):
		return self.path(id).path('suboffers').get(**kwargs).as_objlist(SubOffer)
	
	def add_suboffer(self, id, suboffer, **kwargs):
		params = self.extractor.extract(suboffer,
			required='cpa_policy cost title'.split(),
			optional='auto_approve reentrant'.split()
		)
		params.update(kwargs)
		return self.path(id).path('suboffers').post(**params).as_int()