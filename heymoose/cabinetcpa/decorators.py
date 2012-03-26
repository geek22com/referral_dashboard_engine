from flask import g, redirect, url_for

def advertiser_only(func):
	def _inner(*args, **kwargs):
		if not g.user.is_advertiser:
			return redirect(url_for('cabinetcpa.index'))
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner

def affiliate_only(func):
	def _inner(*args, **kwargs):
		if not g.user.is_affiliate:
			return redirect(url_for('cabinetcpa.index'))
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner