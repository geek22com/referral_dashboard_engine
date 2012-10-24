from heymoose.utils.lang import locked_cached_property


class RegionsRepo(object):
	_exclude_by_code = ('A2',)
	_exclude_by_name = ('None', 'none')

	@locked_cached_property
	def list(self):
		from heymoose import resource as rc
		return [region for region in rc.regions.list()
			if region.country_name not in self._exclude_by_name
			and region.country_code not in self._exclude_by_code]

	@locked_cached_property
	def dict(self):
		return { region.country_code : region for region in self.list }


regions_repo = RegionsRepo()



