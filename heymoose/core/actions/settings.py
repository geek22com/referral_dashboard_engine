from heymoose.core.rest import get, put
from heymoose.utils.shortcuts import dict_update_filled_params
from mappers import settings_from_xml

resource_path = '/settings'

def get_settings():
	return settings_from_xml(get(path=resource_path))


def update_settings(c_min=None, q=None, m=None):
	params = dict()
	dict_update_filled_params(params, cmin=c_min, m=m, q=q)
	return put(path=resource_path, params_dict=params)