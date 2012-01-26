#TODO: generate url smth like this: url('qq').path('id').path('roles')

from heymoose.core.actions.mappers import app_from_xml, count_from_xml
from heymoose.core.rest import post, put, delete, get
from heymoose.utils import convert

resource_path = "/apps"

def add_app(title, user_id, callback, url, platform):
	id = post(path=resource_path,
		params_dict=dict(title=title,
						userId=user_id,
						callback=callback,
                        url=url,
                        platform=platform))
	return int(id)

def update_app(app_id, **kwargs):
	path = "{0}/{1}".format(resource_path, app_id)
	params = dict([(convert.to_camel_case(key), value) for key, value in kwargs.iteritems()])
	put(path=path, params_dict=params)

def delete_app(app_id):
	path = "{0}/{1}".format(resource_path, app_id)
	delete(path=path)

def get_app(app_id, **kwargs):
	path = "{0}/{1}".format(resource_path, app_id)
	return app_from_xml(get(path=path, params_dict=kwargs))

def regenerate_secret(app_id):
	path = "{0}/{1}/secret".format(resource_path, app_id)
	put(path=path)

def active_apps(apps):
	if not apps:
		return None
	active = []
	for app in apps:
		if not app.deleted:
			active.append(app)
	return active

def get_apps(with_deleted=False, user_id=None, **kwargs):
	kwargs.update(withDeleted=with_deleted)
	if user_id: kwargs.update(userId=user_id)
	return map(app_from_xml, get(path=resource_path, params_dict=kwargs))

def get_apps_count(with_deleted=False, user_id=None):
	path = "{0}/{1}".format(resource_path, "count")
	params = dict(withDeleted=with_deleted)
	if user_id: params.update(userId=user_id)
	return count_from_xml(get(path=path, params_dict=params))

