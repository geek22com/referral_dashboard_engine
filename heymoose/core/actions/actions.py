from heymoose.core.actions.mappers import action_from_xml, count_from_xml
from heymoose.core.rest import get, put, delete

resource_path = "/actions"

def get_actions(**kwargs):
	return map(action_from_xml, get(path=resource_path,	params_dict=kwargs))

def get_actions_count():
	path = "{0}/{1}".format(resource_path, "count")
	return count_from_xml(get(path=path))

def get_action(action_id, **kwargs):
	path = "{0}/{1}".format(resource_path, action_id)
	return action_from_xml(get(path=path, params_dict=kwargs))

def approve_action(action_id):
	path = "{0}/{1}".format(resource_path,
	                      action_id)
	put(path=path)

def delete_action(action_id):
	path =  "{0}/{1}".format(resource_path,
	                       action_id)
	delete(path=path)