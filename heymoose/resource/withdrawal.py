from backend import BackendResource
from heymoose.data.models import Debt


class WithdrawalResource(BackendResource):
	base_path = '/withdrawals'

	def list_ordered_withdrawals(self, **kwargs):
		return self.get(**kwargs).as_objlist(Debt, with_count=True)

	def sum_ordered_withdrawals(self):
		return self.path('sum').get().as_obj(Debt)
	
	def list_debts(self, **kwargs):
		return self.path('debt').get(**kwargs).as_objlist(Debt, with_count=True)
		
	def overall_debt(self, **kwargs):
		return self.path('debt').path('sum').get(**kwargs).as_obj(Debt)
	
	def order_withdrawal(self, aff_id):
		self.path('order').put(aff_id=aff_id)
	
	def withdraw(self, **kwargs):
		self.put(**kwargs)