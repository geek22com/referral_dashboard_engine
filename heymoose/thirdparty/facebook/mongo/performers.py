from mongoalchemy.query_expression import QueryExpression
from heymoose.thirdparty.facebook.mongo.data import Performer, Gifts
from heymoose.thirdparty.facebook.mongo.data import AccountAction
from heymoose import mg
from heymoose.thirdparty.facebook.actions import users
from heymoose.utils.workers import app_logger

#TODO: find better case for join analog in Mongo
def get_gifts(performer_id):
	gift_actions = AccountAction.query.filter((AccountAction.performer_id == performer_id).or_(AccountAction.recipient_id == performer_id), AccountAction.operation == 'gift').descending('version').all()
	if not gift_actions:
		return None

	gifts = []
	for action in gift_actions:
		gift = Gifts.query.filter(Gifts.mongo_id == action.gift_id).first()
		if not gift:
			app_logger.debug("get_gifts_i_gifted: critical error There is no gift for performer_id={0} with id={1}".format(performer_id, action.gift_id))
			return None
		if action.performer_id == performer_id: # I gifted
			gifts.append(dict(to_id=action.recipient_id,
								gift=gift))
		elif action.recipient_id == performer_id: # Gifted to me
			gifts.append(dict(from_id=action.performer_id,
								gift=gift))
	return gifts

def get_performer_balance(performer_id):
	action = AccountAction.query.filter(AccountAction.performer_id == performer_id).descending('version').first()
	if not action:
		return 0
	return action.balance

def get_performer(id):
	if not id:
		return None
	return Performer.query.filter(Performer.user_id == id).first()

def is_performer_new(performer_id):
	if not performer_id:
		return False

	performer = Performer.query.filter(Performer.user_id == performer_id).first()
	if performer:
		return False

	return True

def invalidate_performer(performer):
	performer.dirty = True

def contribute_offer_invalidate(performer):
	if not performer:
		return
	if performer.offers_count <= 0:
		app_logger.debug("Breaking attempt or bug: going to contribute_offer_invalidate for peroformer_id={0} offers_count={1}".format(performer.user_id, performer.offers_count))
		return
	performer.offers_count -= 1
	
def contribute_offer(performer):
	if not performer:
		return
	performer.offers_count += 1

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
								gift_id = str(gift.mongo_id),
								operation = "gift")
	new_action.save()
	return True

def create_action_mlm(performer_id, revenue):
	action = AccountAction.query.filter(AccountAction.performer_id == performer_id).descending('version').first()
	if not action and revenue < 0:
		app_logger.debug("create_action_mlm error: attempt to calc negative revenue")
		return False
	if not action:
		new_version = 0
		new_balance = revenue
	else:
		new_version = action.version + 1
		new_balance = action.balance + revenue

	if new_balance < 0:
		app_logger.debug("create_action_mlm error: new_balance < 0")
		return False
	
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
								offer_id = str(offer_id),
								operation = "offer")
	new_action.save()

def get_available_gifts(performer_id):
	action = AccountAction.query.filter(AccountAction.performer_id == performer_id).descending('version').first()
	if not action:
		return None

	gifts = Gifts.query.filter(Gifts.price <= action.balance).all()
	return gifts