from mappers import city_from_xml
from heymoose.core.rest import get, post, put, delete

resource_path = '/cities'


def add_city(name):
	params_dict = dict(name=name)
	id = post(path=resource_path, params_dict=params_dict)
	return int(id)


def update_city(city_id, name):
	path = '{0}/{1}'.format(resource_path, city_id)
	params_dict = dict(name=name)
	put(path=path, params_dict=params_dict)
	
	
def delete_city(city_id):
	path = '{0}/{1}'.format(resource_path, city_id)
	delete(path=path)


def get_cities(**kwargs):
	return map(city_from_xml, get(path=resource_path, params_dict=kwargs))


def get_city(city_id, **kwargs):
	path = "{0}/{1}".format(resource_path, city_id)
	return city_from_xml(get(path=path, params_dict=kwargs))