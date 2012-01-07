from mappers import banner_size_from_xml
from heymoose.core.rest import get, post, put, delete

resource_path = '/banner-sizes'


def add_banner_size(width, height):
	params_dict = dict(width=width,	height=height)
	id = post(path=resource_path, params_dict=params_dict)
	return int(id)


def get_banner_sizes(active_only=True):
	params_dict = dict(activeOnly=active_only)
	return map(banner_size_from_xml, get(path=resource_path, params_dict=params_dict))


def get_banner_size(size_id, **kwargs):
	path = "{0}/{1}".format(resource_path, size_id)
	return banner_size_from_xml(get(path=path, params_dict=kwargs))


def enable_banner_size(size_id):
	path = "{0}/{1}".format(resource_path, size_id)
	put(path=path)
	
def disable_banner_size(size_id):
	path = "{0}/{1}".format(resource_path, size_id)
	delete(path=path)
	
def set_banner_size_enabled(size_id, enabled=True):
	if enabled:
		enable_banner_size(size_id)
	else:
		disable_banner_size(size_id)