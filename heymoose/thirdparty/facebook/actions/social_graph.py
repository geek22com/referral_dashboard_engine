# -*- coding: utf-8 -*-
import json
from heymoose.core.rest import get
from heymoose.thirdparty.facebook.actions.mappers import friends_from_obj
from heymoose.utils.workers import app_logger

GRAPH_BASE = "https://graph.facebook.com"

def get_friends(user_id, access_token):
	path = "/{0}/friends".format(user_id)
	try:
		return friends_from_obj(get(base=GRAPH_BASE,
									path=path,
									params_dict=dict(access_token=access_token),
									renderer=json.loads))
	except Exception as inst:
		#TODO: handle OAuthRequest key error 
		app_logger.debug("get_friends exception={0}".format(type(inst)))
		app_logger.debug(inst)
		raise