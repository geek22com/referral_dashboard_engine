from heymoose.core.actions.mappers import stat_ctr_from_xml
from heymoose.core.rest import get
from heymoose.utils import convert

resource_path = '/stats'

def get_stats_ctr(fm, to, trunc, **kwargs):
	path = '{0}/{1}'.format(resource_path, 'ctr')
	ufm = convert.to_unixtime(fm, True)
	uto = convert.to_unixtime(to, True)
	params = {'from' : ufm, 'to' : uto, 'trunc' : trunc}
	for key, value in kwargs.iteritems():
		params[convert.to_camel_case(key)] = value
	return map(stat_ctr_from_xml, get(path=path, params_dict=params))