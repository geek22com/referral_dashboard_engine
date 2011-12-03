from heymoose.db.models import Invite
from heymoose.utils import gen
from datetime import datetime

def create_invite():
	code = gen.generate_uid(256)
	invite = Invite(code=code, created=datetime.now())
	invite.save()
	return code


def get_invite(code):
	return Invite.query.filter(Invite.code == code, Invite.registered == False).first()
	

def register_invite(code):
	invite = get_invite(code)
	if invite:
		invite.registered = True
		invite.save()
	
	
def delete_unused_invites(before):
	unused = Invite.query.filter(Invite.registered == False, Invite.created < before).all()
	for invite in unused: invite.remove()
	