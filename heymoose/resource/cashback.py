from backend import BackendResource
from heymoose.data.models import Cashback, CashbackInvite


class CashbackResource(BackendResource):
	base_path = '/cashbacks'

	def list(self, aff_id, **kwargs):
		return self.get(aff_id=aff_id, **kwargs).as_objlist(Cashback, with_count=True)

	def list_invites(self, aff_id, **kwargs):
		return self.path('invites').get(aff_id=aff_id, **kwargs).as_objlist(CashbackInvite, with_count=True)