# -*- coding: utf-8 -*-
import json
from restkit.errors import RequestFailed
from heymoose.core.rest import get
from heymoose.thirdparty.facebook.actions.mappers import friends_from_obj
from heymoose.utils.workers import app_logger

GRAPH_BASE = "https://graph.facebook.com"

def get_friends(user_id, access_token):
	path = "/{0}/friends".format(user_id)

	return friends_from_obj(get(base=GRAPH_BASE,
									path=path,
									params_dict=dict(access_token=access_token),
									renderer=json.loads))
