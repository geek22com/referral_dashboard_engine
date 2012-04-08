from backend import BackendResource
from heymoose.data.models import Transaction, AccountingEntry, Withdrawal

class AccountResource(BackendResource):
	base_path = '/account'
	
	def transactions_list(self, id, **kwargs):
		return self.path(id).path('transactions').get(accountId=id, **kwargs).as_objlist(Transaction)
	
	def transactions_count(self, id):
		return self.path(id).path('transactions').path('count').get(accountId=id).as_xmlvalue(int)
	
	def transfer(self, from_id, to_id, amount):
		return self.path('transfer').post(**{ 'from' : from_id, 'to' : to_id, 'amount' : amount })
	
	def entries_list(self, id, **kwargs):
		return self.path(id).path('entries').get(**kwargs).as_objlist(AccountingEntry, with_count=True)
	
	def withdrawals_list(self, id, **kwargs):
		return self.path(id).path('withdraws').get(**kwargs).as_objlist(Withdrawal)
	
	def make_withdrawal(self, id, amount):
		return self.path(id).path('withdraws').post(amount=amount).as_int()
	
	def approve_withdrawal(self, id, withdrawal_id):
		self.path(id).path('withdraws').path(withdrawal_id).put()
	
	def delete_withdrawal(self, id, withdrawal_id, comment):
		self.path(id).path('withdraws').path(withdrawal_id).delete(comment=comment)
		