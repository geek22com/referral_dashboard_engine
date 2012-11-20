from base import notify_user, notify_users
import templates

def offer_blocked(affiliates, offer, reason):
	notify_users(affiliates, templates.OFFER_BLOCKED, offer=offer)
	notify_user(offer.advertiser, templates.OFFER_BLOCKED, offer=offer, reason=reason)

def offer_unblocked(affiliates, offer):
	notify_users(affiliates, templates.OFFER_UNBLOCKED, offer=offer)
	notify_user(offer.advertiser, templates.OFFER_UNBLOCKED, offer=offer)

def grant_approved(grant):
	notify_user(grant.affiliate, templates.GRANT_APPROVED, grant=grant)

def grant_rejected(grant, reason):
	notify_user(grant.affiliate, templates.GRANT_REJECTED, grant=grant, reason=reason)

def grant_blocked(grant, reason):
	notify_user(grant.affiliate, templates.GRANT_BLOCKED, grant=grant, reason=reason)
