# -*- coding: utf-8 -*-
from heymoose import app
import hashlib

request_url = app.config.get('ROBOKASSA_REQUEST_URL')
login = app.config.get('ROBOKASSA_LOGIN')
pass1 = app.config.get('ROBOKASSA_PASS1')
prefix = app.config.get('ROBOKASSA_USER_PREFIX')
default_currency = app.config.get('ROBOKASSA_DEFAULT_CURRENCY')

def signature(sum, inv_id, **params):
	sig_elems = [login, str(sum), str(inv_id), pass1]
	keys = params.keys(); keys.sort()
	for key in keys:
		sig_elems.append('{0}{1}={2}'.format(prefix, key, str(params[key])))
	
	m = hashlib.md5()
	m.update(':'.join(sig_elems).encode('utf-8'))
	return m.hexdigest()

def pay_url(sum, inv_id, email, desc, label=default_currency, **params):
	url = u'{0}?MrchLogin={1}&OutSum={2}&InvId=0&Desc={4}&SignatureValue={5}&IncCurrLabel={6}&Email={7}'.format(
		request_url, login, sum, inv_id, desc, signature(sum, inv_id, **params), label, email)
	for key, value in params.iteritems():
		url += '&{0}{1}={2}'.format(prefix, key, value)
	return url
	
def account_pay_url(account_id, sum, email):
	return pay_url(sum, 0, email, u'Пополнение счета рекламодателя в системе HeyMoose', AccountId=account_id)