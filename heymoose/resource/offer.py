from backend import BackendResource, extractor
from heymoose.data.models import Offer, SubOffer
from restkit.errors import ResourceError, ResourceNotFound


class OfferResource(BackendResource):
	base_path = '/offers'
	
	extractor = extractor().alias(
		advertiser_id='advertiser.id',
		cost='value',
		categories='categories_ids'
	)
	
	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(Offer)
	
	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(Offer, with_count=True)
	
	def get_requested(self, id, aff_id):
		return self.path(id).path('requested').get(aff_id=aff_id).as_obj(Offer)
	
	def get_try_requested(self, id, aff_id):
		try:
			return self.get_requested(id, aff_id)
		except ResourceNotFound:
			return self.get_by_id(id)
	
	def list_requested(self, aff_id, **kwargs):
		return self.path('requested').get(aff_id=aff_id, **kwargs).as_objlist(Offer, with_count=True)
	
	def add(self, offer, balance, **kwargs):
		params = self.extractor.extract(offer,
			required='advertiser_id pay_method cost name description url title code hold_days cookie_ttl'.split(),
			nonempty='regions'.split(),
			optional='cpa_policy allow_negative_balance auto_approve reentrant logo_filename categories'.split()
		)
		params.update(balance=balance)
		params.update(kwargs)
		return self.post(**params).as_int()
	
	def block(self, id, reason):
		self.path(id).path('blocked').put(reason=reason)
	
	def unblock(self, id):
		self.path(id).path('blocked').delete()
	
	def list_suboffers(self, id, **kwargs):
		return self.path(id).path('suboffers').get(**kwargs).as_objlist(SubOffer)
	
	def add_suboffer(self, id, suboffer, **kwargs):
		params = self.extractor.extract(suboffer,
			required='cpa_policy cost title code hold_days'.split(),
			optional='auto_approve reentrant'.split()
		)
		params.update(kwargs)
		return self.path(id).path('suboffers').post(**params).as_int()
	
	def add_banner(self, id, banner, image, **kwargs):
		params = self.extractor.extract(banner, required='width height mime_type'.split())
		params.update(image=image)
		params.update(kwargs)
		return self.path(id).path('banners').post(**params).as_int()
	
	def delete_banner(self, id, banner_id):
		self.path(id).path('banners').path(banner_id).delete()
	
	def check_code(self, advertiser_id, code):
		try:
			self.path('code').put(advertiser_id=advertiser_id, code=code)
			return True
		except ResourceError:
			return False