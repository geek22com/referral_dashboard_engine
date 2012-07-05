class RegionsRepo(object):
	_regions = None
	_regions_dict = None
	_exclude_by_code = ('A2',)
	_exclude_by_name = ('None', 'none')
	
	def _fetch(self):
		from heymoose import resource as rc
		self._regions = [region for region in rc.regions.list()
			if region.country_name not in self._exclude_by_name
			and region.country_code not in self._exclude_by_code]
		self._regions = sorted(self._regions, key=lambda r: r.country_name)
		self._regions_dict = { region.country_code : region for region in self._regions }
	
	def as_list(self):
		if not self._regions:
			self._fetch()
		return self._regions
	
	def as_dict(self):
		if not self._regions_dict:
			self._fetch()
		return self._regions_dict


regions_repo = RegionsRepo()



