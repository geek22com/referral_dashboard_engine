from backend import BackendResource
from heymoose.data.models import UserStat

class UserStatResource(BackendResource):
	base_path = '/user-stats'

	def list_fraud(self, **kwargs):
		return self.path('fraud').get(**kwargs).as_objlist(UserStat, with_count=True)