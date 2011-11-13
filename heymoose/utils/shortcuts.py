from flask import abort
from restkit.errors import ResourceError
from math import ceil

def do_or_abort(func, *args, **kwargs):
	try:
		return func(*args, **kwargs)
	except ResourceError as e:
		abort(e.status_int)
	except:
		abort(500)
		
		
def paginate(page, count, per_page):
	offset = (page - 1) * per_page
	limit = min(page * per_page, count)
	pcount = int(ceil(float(count) / per_page)) if per_page > 0 else 0
	if pcount == 0: pcount = 1
	return offset, limit, dict(current=page, count=pcount)
		