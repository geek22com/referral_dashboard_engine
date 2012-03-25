from flask import g, redirect, url_for

def customer_only(func):
	def _inner(*args, **kwargs):
		if not g.user.is_customer():
			return redirect(url_for('cabinet.index'))
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner

def developer_only(func):
	def _inner(*args, **kwargs):
		if not g.user.is_developer():
			return redirect(url_for('cabinet.index'))
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner

'''def partner_only(func):
	def _inner(*args, **kwargs):
		#if not g.user.is_partner():
		if not g.user.email in ('d1@d.ru', 'mratozar@gmail.com'):
			return redirect(url_for('cabinet.index'))
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner'''

partner_only = developer_only
advertiser_only = customer_only


def banner_network_only(func):
	def _inner(*args, **kwargs):
		if not g.user.is_developer() or not g.user.is_customer():
			return redirect(url_for('cabinet.index'))
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner

cpa_network_only = banner_network_only