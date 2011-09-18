from heymoose.core.actions.mappers import action_from_xml
from heymoose.core.rest import get, put, delete
from heymoose.utils.workers import app_logger

resource_path = "/actions"

def get_actions(offset, limit):
	app_logger.debug()
	return map(action_from_xml, get(path=resource_path,
									params_dict=dict(offset=offset,
									limit=limit)))

def approve_action(action_id):
	app_logger.debug()
	path = "%s/%d".format(resource_path,
	                      action_id)
	put(path=path)

def delete_action(action_id):
	app_logger.debug()
	path =  "%s/%d".format(resource_path,
	                       action_id)
	delete(path=path)