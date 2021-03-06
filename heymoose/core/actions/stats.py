from heymoose.core.actions.mappers import stat_from_xml
from heymoose.core.rest import get
from heymoose.utils import convert
from heymoose.utils.shortcuts import dict_update_filled_params

resource_path = '/stats'

def get_stats_ctr(fm, to, trunc, **kwargs):
	path = '{0}/{1}'.format(resource_path, 'ctr')
	ufm = convert.to_unixtime(fm, True)
	uto = convert.to_unixtime(to, True)
	params = {'from' : ufm, 'to' : uto, 'trunc' : trunc}
	for key, value in kwargs.iteritems():
		params[convert.to_camel_case(key)] = value
	return map(stat_from_xml, get(path=path, params_dict=params))


def get_stats_ctr_by_ids(offer_ids=None, app_ids=None, fm=None, to=None):
	path = '{0}/{1}'.format(resource_path, 'ctr-by-ids')
	ufm = convert.to_unixtime(fm, True) if fm else None
	uto = convert.to_unixtime(to, True) if to else None
	params = dict()
	dict_update_filled_params(params, **{ 'offer' : offer_ids, 'app' : app_ids, 'from' : ufm, 'to' : uto })
	return map(stat_from_xml, get(path=path, params_dict=params))


def get_stats_audience(resource, offer_id=None, app_id=None, fm=None, to=None):
	path = '{0}/audience/{1}'.format(resource_path, resource)
	ufm = convert.to_unixtime(fm, True) if fm else None
	uto = convert.to_unixtime(to, True) if to else None
	params = dict()
	dict_update_filled_params(params, **{ 'offerId' : offer_id, 'appId' : app_id, 'from' : ufm, 'to' : uto })
	return map(stat_from_xml, get(path=path, params_dict=params))

def get_stats_audience_by_genders(offer_id=None, app_id=None, fm=None, to=None):
	return get_stats_audience('by-genders', offer_id, app_id, fm, to)

def get_stats_audience_by_cities(offer_id=None, app_id=None, fm=None, to=None):
	return get_stats_audience('by-cities', offer_id, app_id, fm, to)

def get_stats_audience_by_years(offer_id=None, app_id=None, fm=None, to=None):
	return get_stats_audience('by-years', offer_id, app_id, fm, to)