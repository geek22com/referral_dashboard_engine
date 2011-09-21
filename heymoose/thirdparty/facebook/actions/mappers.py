# -*- coding: utf-8 -*-

def token_from_obj(acces_token_obj):
	if len(acces_token_obj['access_token']) == 0:
		return None
	return acces_token_obj['access_token'][0]

def expires_from_obj(acces_token_obj):
	if len(acces_token_obj['expires']) == 0:
		return None
	return acces_token_obj['expires'][0]

def friends_from_obj(friends_obj):
	if len(friends_obj['data']) == 0:
		return None
	return friends_obj['data']