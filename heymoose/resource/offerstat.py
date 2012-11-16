from backend import BackendResource
from heymoose.data.models import OverallOfferStat, TotalStat


class OfferStatResource(BackendResource):
	base_path = '/stats'
	
	def list_aff(self, **kwargs):
		return self.path('offers').path('aff').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_adv(self, **kwargs):
		return self.path('offers').path('adv').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_all(self, **kwargs):
		return self.path('offers').path('all').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_user(self, user, **kwargs):
		if user.is_affiliate:
			return self.list_aff(aff_id=user.id, **kwargs)
		elif user.is_advertiser:
			return self.list_adv(adv_id=user.id, **kwargs)
		else:
			return [], 0
	
	def list_advertiser(self, **kwargs):
		return self.path('advertisers').path('all').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_affiliate(self, **kwargs):
		return self.path('affiliates').path('all').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_affiliate_top(self, **kwargs):
		return self.path('affiliates').path('top').get(**kwargs).as_objlist(OverallOfferStat)
	
	def list_affiliate_by_offer(self, **kwargs):
		return self.path('affiliates').path('offer').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_by_sub_id(self, **kwargs):
		return self.path('sub_ids').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_by_source_id(self, **kwargs):
		return self.path('source_ids').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_by_referer(self, **kwargs):
		return self.path('referer').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_by_keywords(self, **kwargs):
		return self.path('keywords').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)

	def list_by_cashback(self, **kwargs):
		return self.path('cashbacks').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer(self, **kwargs):
		return self.path('suboffers').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer_by_affiliate(self, **kwargs):
		return self.path('suboffers').path('affiliate').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer_by_advertiser(self, **kwargs):
		return self.path('suboffers').path('advertiser').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer_by_sub_id(self, **kwargs):
		return self.path('suboffers').path('sub_id').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer_by_source_id(self, **kwargs):
		return self.path('suboffers').path('source_id').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer_by_referer(self, **kwargs):
		return self.path('suboffers').path('referer').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_suboffer_by_keywords(self, **kwargs):
		return self.path('suboffers').path('keywords').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)

	def list_suboffer_by_cashback(self, **kwargs):
		return self.path('suboffers').path('cashback').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def total(self, **kwargs):
		return self.path('total').get(**kwargs).as_obj(TotalStat)