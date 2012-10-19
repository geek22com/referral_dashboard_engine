from functools import wraps
from flask import render_template, request
from heymoose.utils.pagination import current_page, page_limits, paginate

def template(template_name):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			rv = f(*args, **kwargs)
			return render_template(template_name, **rv) if isinstance(rv, dict) else rv
		return wrapped
	return decorator

def context(provider):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			additional_context = provider(*args, **kwargs)
			kwargs.update(additional_context)
			rv = f(*args, **kwargs)
			if isinstance(rv, dict):
				rv.update(additional_context)
			return rv
		return wrapped
	return decorator

def sorted(default_order=None, default_direction=None, order_arg='ord', direction_arg='dir'):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			order = request.args.get(order_arg, default_order)
			direction = request.args.get(direction_arg, default_direction) if order else None
			if order and direction:
				kwargs.update(ordering=order.upper(), direction=direction.upper())
			rv = f(*args, **kwargs)
			if isinstance(rv, dict):
				rv.update(order=order, direction=direction)
			return rv
		return wrapped
	return decorator

def paginated(per_page=20, page_arg='page'):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			page = current_page(page_arg)
			offset, limit = page_limits(page, per_page)
			rv = f(*args, offset=offset, limit=limit, **kwargs)
			if isinstance(rv, dict):
				pages = paginate(page, rv.get('count', 0), per_page)
				rv.update(pages=pages)
			return rv
		return wrapped
	return decorator
