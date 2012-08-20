from base import notify_user, notify_offer_affiliates, notify_all
import templates

def offer_blocked(offer, reason):
	notify_offer_affiliates(offer, templates.OFFER_BLOCKED)
	notify_user(offer.advertiser, templates.OFFER_BLOCKED, offer=offer, reason=reason)

def offer_unblocked(offer):
	notify_offer_affiliates(offer, templates.OFFER_UNBLOCKED)
	notify_user(offer.advertiser, templates.OFFER_UNBLOCKED, offer=offer)

def grant_approved(grant):
	notify_user(grant.affiliate, templates.GRANT_APPROVED, grant=grant)

def grant_rejected(grant, reason):
	notify_user(grant.affiliate, templates.GRANT_REJECTED, grant=grant, reason=reason)

def grant_blocked(grant, reason):
	notify_user(grant.affiliate, templates.GRANT_BLOCKED, grant=grant, reason=reason)
