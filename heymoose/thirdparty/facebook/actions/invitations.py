from heymoose.thirdparty.facebook.actions import social_graph, oauth
from heymoose.thirdparty.facebook.mongo import invites
from heymoose.core.actions import invitations
from heymoose.utils.workers import app_logger

def check_invite(performer_id):
	if not performer_id:
		return None

	app_access_token = oauth.get_app_access_token()
	if not app_access_token:
		app_logger.debug("check_invite: can't get app_access_token performer_id={0}".format(performer_id))
		return None

	apprequests = social_graph.get_apprequests(performer_id, app_access_token)
	if not apprequests:
		return None

	inviter = apprequests[0]
	return inviter["from"]["id"]

def confirm_invite(performer_id, from_id, app_id):
	invites.create_invite(from_id=from_id,
							to_id=performer_id)

	invitations.add_mlm_invite(from_id=from_id,
								to_id=performer_id,
								app_id=app_id)

  