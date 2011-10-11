from heymoose.core.rest import post

resource_path = "/performers"

def add_mlm_invite(from_id, to_id, app_id):
	post(path=resource_path,
		params_dict=dict(extId=to_id,
						inviterExtId=from_id,
						appId=app_id))
  