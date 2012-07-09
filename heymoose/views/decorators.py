from functools import wraps
from flask import render_template, request
from heymoose.utils.pagination import current_page, page_limits, paginate

def template(template_name):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			context = f(*args, **kwargs)
			return render_template(template_name, **context) if isinstance(context, dict) else context
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
			context = f(*args, **kwargs)
			if isinstance(context, dict):
				context.update(order=order, direction=direction)
			return context
		return wrapped
	return decorator

def paginated(per_page=20, page_arg='page'):
	def decorator(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			page = current_page(page_arg)
			offset, limit = page_limits(page, per_page)
			context = f(*args, offset=offset, limit=limit, **kwargs)
			if isinstance(context, dict):
				pages = paginate(page, context.get('count', 0), per_page)
				context.update(pages=pages)
			return context
		return wrapped
	return decorator
