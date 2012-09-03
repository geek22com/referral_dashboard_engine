from backend import BackendResource
from heymoose.data.models import AffiliateTopEntry


class PublicResource(BackendResource):
	base_path = '/public'
	
	def offer_count(self):
		return self.path('offer').path('count').get().as_int()
	
	def top_withdrawals(self):
		return self.path('affiliate').path('top-withdraw').get().as_objlist(AffiliateTopEntry)
	
	def top_conversion(self):
		return self.path('affiliate').path('top-conversion').get().as_objlist(AffiliateTopEntry)