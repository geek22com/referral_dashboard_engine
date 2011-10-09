from heymoose.thirdparty.facebook.mongo.data import Performer, Gifts
from heymoose.thirdparty.facebook.mongo.data import AccountAction
from heymoose import mg
from heymoose.thirdparty.facebook.actions import users
from heymoose.utils.workers import app_logger

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

def create_action_gift(performer, gift, recipient_id):
	action = AccountAction.query.filter(AccountAction.performer_id == performer.user_id).descending('version').first()
	if not action:
		return False # User no money

	if gift.price > action.balance:
		return False # Too expensive

	new_action = AccountAction(version = action.version + 1,
								balance = action.balance - gift.price,
								performer_id = performer.user_id,
								recipient_id = recipient_id,
								gift_id = gift.mongo_id,
								operation = "gift")
	new_action.save()
	return True

def create_action_mlm(performer_id, revenue):
	action = AccountAction.query.filter(AccountAction.performer_id == performer_id).descending('version').first()
	if not action:
		app_logger.debug("Error: try to make negative balance performer_id:{0}".format(performer_id))
		return False
	else:
		new_version = action.version + 1
		new_balance = action.balance + revenue

	new_action = AccountAction(version = new_version,
								balance = new_balance,
								performer_id = performer_id,
								operation = "mlm")
	new_action.save()
	return True


def create_action_offer(performer_id, offer_id, cost):
	action = AccountAction.query.filter(AccountAction.performer_id == performer_id).descending('version').first()
	if not action:
		new_version = 0
		new_balance = cost
	else:
		new_version = action.version + 1
		new_balance = action.balance + cost

	new_action = AccountAction(version = new_version,
								balance = new_balance,
								performer_id = performer_id,
								offer_id = offer_id,
								operation = "offer")
	new_action.save()

def get_available_gifts(performer):
	action = AccountAction.query.filter(AccountAction.performer_id == performer.user_id).descending('version').first()
	if not action:
		return None

	gifts = Gifts.query.filter(Gifts.price <= action.balance).all()
	return gifts