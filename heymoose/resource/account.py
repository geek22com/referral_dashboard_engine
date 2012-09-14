from backend import BackendResource
from heymoose.data.models import Transaction, AccountingEntry, Withdrawal, WithdrawalList, Debt

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
	
	def withdrawals_list(self, **kwargs):
		return self.path('withdraws').get(**kwargs).as_obj(WithdrawalList)
	
	def withdrawals_list_by_account(self, id, **kwargs):
		return self.path(id).path('withdraws').get(**kwargs).as_objlist(Withdrawal)
	
	def withdrawals_list_by_affiliate(self, id, **kwargs):
		return self.path('aff').path(id).path('withdraws').get(**kwargs).as_objlist(Withdrawal)
	
	def create_withdrawal(self, id):
		return self.path(id).path('withdraws').post().as_int()
	
	def approve_withdrawal(self, id):
		self.path('withdraws').path(id).put()
	
	def delete_withdrawal(self, id, comment):
		self.path('withdraws').path(id).delete(comment=comment)
		
	def list_debt_by_affiliate(self, offer_id, **kwargs):
		return self.path('debt').path('by_affiliate').get(offer_id=offer_id, **kwargs).as_objlist(Debt, with_count=True)
	
	def list_debt_by_offer(self, affiliate_id, **kwargs):
		return self.path('debt').path('by_offer').get(affiliate_id=affiliate_id, **kwargs).as_objlist(Debt, with_count=True)
		