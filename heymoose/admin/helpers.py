# -*- coding: utf-8 -*-
from functools import wraps
from flask import g, request, redirect, url_for, flash


def not_enough_permissions():
	flash(u'У вас недостаточно прав для совершения этого действия', 'danger')
	admin_index_url = url_for('.index')
	return redirect(request.referrer if request.referrer and admin_index_url in request.referrer else admin_index_url)


def superadmin_required(post=False):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if (post or request.method != 'POST') and not g.user.is_superadmin:
				return not_enough_permissions()
			return f(*args, **kwargs)
		return wrapped
	return decorator


def permission_required(permission, post=False):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if (post or request.method != 'POST') and not g.user.can(permission):
				return not_enough_permissions()
			return f(*args, **kwargs)
		return wrapped
	return decorator