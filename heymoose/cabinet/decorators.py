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