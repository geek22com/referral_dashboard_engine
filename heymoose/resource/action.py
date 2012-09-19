from backend import BackendResource
from heymoose.data.models import OfferAction

class ActionResource(BackendResource):
	base_path = '/actions'
	
	def approve_expired(self, **kwargs):
		return self.put(**kwargs).as_int()
	
	def cancel_by_transactions(self, offer_id, transactions):
		return self.delete(offer_id=offer_id, transactions=transactions).as_int()
	
	def approve_by_ids(self, offer_id, ids):
		self.path('by_id').put(offer_id=offer_id, id=ids)
	
	def cancel_by_ids(self, offer_id, ids):
		self.path('by_id').delete(offer_id=offer_id, id=ids)
	
	def list(self, offer_id, **kwargs):
		return self.get(offer_id=offer_id, **kwargs).as_objlist(OfferAction, with_count=True)
		