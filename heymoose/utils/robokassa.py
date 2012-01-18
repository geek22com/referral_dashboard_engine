from heymoose import app
import hashlib

request_url = app.config.get('ROBOKASSA_REQUEST_URL')
login = app.config.get('ROBOKASSA_LOGIN')
pass1 = app.config.get('ROBOKASSA_PASS1')
prefix = app.config.get('ROBOKASSA_USER_PREFIX')
default_currency = app.config.get('ROBOKASSA_DEFAULT_CURRENCY')

def signature(account_id, sum, **params):
	sig_elems = [login, str(sum), str(account_id), pass1]
	keys = params.keys(); keys.sort()
	for key in keys:
		sig_elems.append('{0}{1}={2}'.format(prefix, key, str(params[key])))
	
	m = hashlib.md5()
	m.update(':'.join(sig_elems).encode('utf-8'))
	return m.hexdigest()

def pay_url(account_id, sum, email, desc, label=default_currency, **params):
	url = u'{0}?MrchLogin={1}&OutSum={2}&InvId={3}&Desc={4}&SignatureValue={5}&IncCurrLabel={6}'.format(
		request_url, login, sum, account_id, desc, signature(account_id, sum, **params), label)
	for key, value in params.iteritems():
		url += '&{0}{1}={2}'.format(prefix, key, value)
	return url
	