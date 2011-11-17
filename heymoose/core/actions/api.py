from heymoose.core.rest import get
import hashlib

resource_path = "/api"

def signed_params(params, secret):
	keys = params.keys()[:]
	keys.sort()
	
	result = ''
	for key in keys:
		result += '{0}={1}'.format(key, str(params[key]))
		
	m = hashlib.md5()
	m.update(result + secret)
	return m.hexdigest()

def api_get(params, secret):
	params.update(sig=signed_params(params, secret))
	return get(path=resource_path, params_dict=params, renderer=unicode)

# For debug perposes
def do_offer(offer_id, app_id, uid, platform, secret):
	params = dict(
		method='doOffer',
		app_id=app_id,
		offer_id=offer_id,
		uid=uid,
		platform=platform)
	return api_get(params, secret)

def get_offers(app_id, uid, secret):
	params = dict(
		method='getOffers',
		app_id=app_id,
		uid=uid)
	return api_get(params, secret)
	