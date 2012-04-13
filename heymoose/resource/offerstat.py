from backend import BackendResource
from heymoose.data.models import OverallOfferStat


class OfferStatResource(BackendResource):
	base_path = '/stats'
	
	def list(self, **kwargs):
		return self.get(**kwargs).as_objlist(OverallOfferStat, with_count=True)