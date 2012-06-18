from backend import BackendResource
from heymoose.data.models import OverallOfferStat


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
	
	def list_affiliate(self, **kwargs):
		return self.path('affiliates').path('all').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	def list_affiliate_top(self, **kwargs):
		return self.path('affiliates').path('top').get(**kwargs).as_objlist(OverallOfferStat)
	
	def list_affiliate_by_offer(self, **kwargs):
		return self.path('affiliates').path('offer').get(**kwargs).as_objlist(OverallOfferStat, with_count=True)
	
	