# -*- coding: utf-8 -*-
from heymoose.utils.config import config_value
import hashlib

def signature(sum, inv_id, **params):
	login = config_value('ROBOKASSA_LOGIN')
	pass1 = config_value('ROBOKASSA_PASS1')
	prefix = config_value('ROBOKASSA_USER_PREFIX')
	sig_elems = [login, str(sum), str(inv_id), pass1]
	keys = params.keys(); keys.sort()
	for key in keys:
		sig_elems.append('{0}{1}={2}'.format(prefix, key, str(params[key])))
	
	m = hashlib.md5()
	m.update(':'.join(sig_elems).encode('utf-8'))
	return m.hexdigest()

def pay_url(sum, inv_id, email, desc, **params):
	login = config_value('ROBOKASSA_LOGIN')
	prefix = config_value('ROBOKASSA_USER_PREFIX')
	request_url = config_value('ROBOKASSA_REQUEST_URL')
	default_currency = config_value('ROBOKASSA_DEFAULT_CURRENCY')
	url = u'{0}?MrchLogin={1}&OutSum={2}&InvId=0&Desc={4}&SignatureValue={5}&IncCurrLabel={6}&Email={7}'.format(
		request_url, login, sum, inv_id, desc, signature(sum, inv_id, **params), default_currency, email)
	for key, value in params.iteritems():
		url += '&{0}{1}={2}'.format(prefix, key, value)
	return url
	
def account_pay_url(account_id, sum, email):
	return pay_url(sum, 0, email, u'Пополнение счета рекламодателя в системе HeyMoose', AccountId=account_id)