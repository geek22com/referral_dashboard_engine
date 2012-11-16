from backend import BackendResource
from heymoose.data.models import CashBack


class CashBackResource(BackendResource):
	base_path = '/cashbacks'

	def list(self, aff_id, **kwargs):
		return self.get(aff_id=aff_id, **kwargs).as_objlist(CashBack, with_count=True)