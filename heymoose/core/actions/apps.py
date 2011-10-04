#TODO: generate url smth like this: url('qq').path('id').path('roles')

from heymoose.core.actions.mappers import app_from_xml
from heymoose.core.rest import post, put
from heymoose.utils.workers import app_logger

resource_path = "/apps"

def add_app(user_id, callback):
	post(path=resource_path,
		params_dict=dict(userId=user_id,
						callback=callback))

def get_app(app_id):
	path = "{0}/{1}".format(resource_path, app_id)
	return app_from_xml(get(path=path))

def regenerate_secret(app_id):
	path = "{0}/{1}".format(resource_path, app_id)
	put(path=path)
