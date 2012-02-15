from heymoose.core.rest import get, put
from heymoose.utils.shortcuts import dict_update_filled_params
from mappers import settings_from_xml

resource_path = '/settings'

def get_settings():
	return settings_from_xml(get(path=resource_path))


def update_settings(m=None, q=None, d_avg=None):
	params = dict()
	dict_update_filled_params(params, M=m, Q=q, Davg=d_avg)
	return put(path=resource_path, params_dict=params)