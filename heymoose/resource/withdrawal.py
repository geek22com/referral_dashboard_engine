from backend import BackendResource
from heymoose.data.models import Debt


class WithdrawalResource(BackendResource):
	base_path = '/withdrawals'
	
	def list_debt_by_affiliate(self, offer_id, **kwargs):
		return self.path('debt').path('by_affiliate').get(offer_id=offer_id, **kwargs).as_objlist(Debt, with_count=True)
	
	def list_debt_by_offer(self, aff_id, **kwargs):
		return self.path('debt').path('by_offer').get(aff_id=aff_id, **kwargs).as_objlist(Debt, with_count=True)
	
	def overall_debt(self, **kwargs):
		return self.path('debt').get(**kwargs).as_obj(Debt)
	
	def order_withdrawal(self, aff_id):
		self.path('order').put(aff_id=aff_id)
	
	def withdraw(self, **kwargs):
		self.put(**kwargs)