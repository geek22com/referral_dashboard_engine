from backend import BackendResource

class ActionResource(BackendResource):
	base_path = '/actions'
	
	def approve_expired(self, **kwargs):
		return self.put(**kwargs).as_int()
	
	def cancel_by_transactions(self, offer_id, transactions):
		return self.delete(offer_id=offer_id, transactions=transactions).as_int()