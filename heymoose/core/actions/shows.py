from heymoose.core.actions.mappers import order_show_from_xml
from heymoose.core.rest import get
from heymoose.utils import convert

resource_path = '/shows'

# Available kwargs: offerId, appId, performerId
def get_shows_range(fm, to, **kwargs):
	ufm = convert.to_unixtime(fm)
	uto = convert.to_unixtime(to)
	kwargs.update({'from' : ufm, 'to' : uto})
	return map(order_show_from_xml, get(path=resource_path, params_dict=kwargs))
	
	