from backend import BackendResource
from heymoose.data.models import DebtsList


class WithdrawalResource(BackendResource):
	base_path = '/withdrawals'
	
	def list_debt_by_affiliate(self, offer_id, **kwargs):
		return self.path('debt').path('by_affiliate').get(offer_id=offer_id, **kwargs).as_obj(DebtsList)
	
	def list_debt_by_offer(self, affiliate_id, **kwargs):
		return self.path('debt').path('by_offer').get(affiliate_id=affiliate_id, **kwargs).as_obj(DebtsList)
	
	def withdraw(self, **kwargs):
		self.put(**kwargs)