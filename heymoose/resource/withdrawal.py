from backend import BackendResource
from heymoose.data.models import Debt, AffiliatePayment


class WithdrawalResource(BackendResource):
	base_path = '/withdrawals'

	def list_ordered_by_affiliate(self, **kwargs):
		return self.get(**kwargs).as_objlist(Debt, with_count=True)

	def list_ordered_by_offer(self, **kwargs):
		return self.path('by_offer').get(**kwargs).as_objlist(Debt, with_count=True)

	def sum_ordered(self):
		return self.path('sum').get().as_obj(Debt)
	
	def list_debts(self, **kwargs):
		return self.path('debt').get(**kwargs).as_objlist(Debt, with_count=True)
		
	def overall_debt(self, **kwargs):
		return self.path('debt').path('sum').get(**kwargs).as_obj(Debt)
	
	def order_withdrawal(self, aff_id):
		self.path('order').put(aff_id=aff_id)
	
	def withdraw(self, **kwargs):
		self.put(**kwargs)

	def list_payments(self, **kwargs):
		return self.path('payments').get(**kwargs).as_objlist(AffiliatePayment, with_count=True)