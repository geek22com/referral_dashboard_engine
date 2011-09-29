from heymoose.thirdparty.facebook.mongo.data import Performer
def get_performer(id):
	if not id:
		return None
	return Performer.query.filter(Performer.user_id == id).first()

def invalidate_performer(performer):
	performer.dirty = True