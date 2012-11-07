from backend import BackendResource, extractor
from heymoose.data.models import Offer, SubOffer
from heymoose.utils.convert import to_unixtime
from restkit.errors import ResourceError, ResourceNotFound

def extract_categories(offer):
	return [c.id for c in offer.categories] if offer.categories is not None else None, offer.is_dirty('categories')

def extract_regions(offer):
	return list(offer.regions), offer.is_dirty('regions')

def extract_launch_time(offer):
	return to_unixtime(offer.launch_time, msec=True), offer.is_dirty('launch_time')

class OfferResource(BackendResource):
	base_path = '/offers'
	
	extractor = extractor().alias(
		advertiser_id='advertiser.id',
		categories=extract_categories,
		regions=extract_regions,
		launch_time=extract_launch_time
	)
	
	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(Offer)

	def get_referral_offer(self, **kwargs):
		try:
			return self.path('referral').get(**kwargs).as_obj(Offer)
		except:
			return None

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
			required='''advertiser_id pay_method name description short_description url site_url
				title code hold_days cookie_ttl launch_time'''.split(),
			optional='''cpa_policy cost cost2 percent allow_negative_balance auto_approve reentrant
				logo_filename categories regions allow_deeplink'''.split()
		)
		params.update(balance=balance)
		params.update(kwargs)
		return self.post(**params).as_int()
	
	def update(self, offer, **kwargs):
		params = self.extractor.extract(offer,
			updated='''pay_method cpa_policy cost cost2 percent title code hold_days auto_approve reentrant
				name description short_description cr url site_url cookie_ttl categories regions allow_negative_balance
				showcase logo_filename token_param_name launch_time allow_deeplink yml_url'''.split()
		)
		params.update(kwargs)
		self.path(offer.id).put(**params)
	
	def block(self, id, reason):
		self.path(id).path('blocked').put(reason=reason)
	
	def unblock(self, id):
		self.path(id).path('blocked').delete()
	
	def list_suboffers(self, id, **kwargs):
		return self.path(id).path('suboffers').get(**kwargs).as_objlist(SubOffer)
	
	def add_suboffer(self, id, suboffer, **kwargs):
		params = self.extractor.extract(suboffer,
			required='cpa_policy title code hold_days'.split(),
			optional='auto_approve cost cost2 percent reentrant'.split()
		)
		params.update(kwargs)
		return self.path(id).path('suboffers').post(**params).as_int()
	
	def update_suboffer(self, id, suboffer, **kwargs):
		params = self.extractor.extract(suboffer,
			updated='cpa_policy cost cost2 percent title code hold_days auto_approve reentrant active'.split()
		)
		params.update(kwargs)
		self.path(id).path('suboffers').path(suboffer.id).put(**params)
	
	def add_banner(self, id, banner, image, **kwargs):
		params = self.extractor.extract(banner, required='width height mime_type'.split())
		params.update(image=image)
		params.update(kwargs)
		return self.path(id).path('banners').post(**params).as_int()
	
	def update_banner(self, id, banner, **kwargs):
		params = self.extractor.extract(banner, updated=['url'])
		params.update(kwargs)
		self.path(id).path('banners').path(banner.id).put(**params)
	
	def delete_banner(self, id, banner_id):
		self.path(id).path('banners').path(banner_id).delete()
	
	def check_code(self, advertiser_id, code, **kwargs):
		try:
			self.path('code').put(advertiser_id=advertiser_id, code=code, **kwargs)
			return True
		except ResourceError:
			return False
	
	def add_to_balance(self, id, amount):
		self.path(id).path('account').put(amount=amount)
	
	def remove_from_balance(self, id, amount):
		self.path(id).path('account').delete(amount=amount)