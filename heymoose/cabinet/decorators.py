from flask import g, abort

def customer_only(func):
	def _inner(*args, **kwargs):
		if not hasattr(g, 'user') or g.user is None or not g.user.is_customer():
			abort(403)
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner

def developer_only(func):
	def _inner(*args, **kwargs):
		if not hasattr(g, 'user') or g.user is None or not g.user.is_developer():
			abort(403)
		return func(*args, **kwargs)
	_inner.__name__ = func.__name__
	return _inner