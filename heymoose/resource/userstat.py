from backend import BackendResource
from heymoose.data.models import UserStat, ReferralStat

class UserStatResource(BackendResource):
	base_path = '/user-stats'

	def list_fraud(self, **kwargs):
		return self.path('fraud').get(**kwargs).as_objlist(UserStat, with_count=True)

	def list_referrals(self, aff_id, **kwargs):
		return self.path(aff_id).path('referrals').get(**kwargs).as_objlist(ReferralStat, with_count=True)