from heymoose.thirdparty.facebook.mongo.data import Invitations, Performer

def create_invite(from_id, to_id):
	invitation = Invitations(from_id=str(from_id),
								to_id=str(to_id))
	invitation.save()

def get_invites(performer_id):
	cur_invites = Invitations.query.filter((Invitations.from_id == performer_id).or_(Invitations.to_id == performer_id)).descending('date').all()
	if not cur_invites:
		return None
	return cur_invites