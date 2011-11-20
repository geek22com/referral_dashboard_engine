from mappers import performer_from_xml, count_from_xml
from heymoose.core.rest import get

resource_path = "/performers"

def get_performer(performer_id, **kwargs):
	path = '{0}/{1}'.format(resource_path, performer_id)
	return performer_from_xml(get(path=path, params_dict=kwargs))


def get_performers(**kwargs):
	return map(performer_from_xml, get(path=resource_path, params_dict=kwargs))


def get_performers_count():
	path = "{0}/{1}".format(resource_path, "count")
	return count_from_xml(get(path=path))