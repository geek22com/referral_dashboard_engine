from heymoose.thirdparty.facebook.mongo.data import Performer
from heymoose.thirdparty.facebook.actions import users
def get_performer(id):
	if not id:
		return None
	return Performer.query.filter(Performer.user_id == id).first()

def invalidate_performer(performer):
	performer.dirty = True

def reload_performer_info(performer, fresh_performer_obj):
	performer.fullname = fresh_performer_obj[u'name']
	performer.firstname = fresh_performer_obj[u'first_name']
	performer.lastname = fresh_performer_obj[u'last_name']
	performer.dirty = False