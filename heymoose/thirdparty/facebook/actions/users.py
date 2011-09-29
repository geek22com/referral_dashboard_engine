# -*- coding: utf-8 -*-
import json
from heymoose.core.rest import get
from heymoose import config

def get_user(user_id, access_token):
	path = "/{0}".format(user_id)

	return get(base=config.get('FACEBOOK_GRAPH_URL'),
				path=path,
				params_dict=dict(access_token=access_token),
				renderer=json.loads)
