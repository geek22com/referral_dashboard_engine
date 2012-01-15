from flask import abort
from heymoose import app
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
	limit = per_page
	pcount = int(ceil(float(count) / per_page)) if per_page > 0 else 0
	if pcount == 0: pcount = 1
	
	# Calculate pages range
	zone = app.config.get('ADMIN_PAGES_RANGE', 7)
	pfirst = page - zone
	plast = page + zone
	
	if pfirst < 1 and plast > pcount:
		pfirst = 1
		plast = pcount
	elif pfirst < 1:
		pfirst = 1
		plast = min(pfirst + 2 * zone, pcount)
	elif plast > pcount:
		plast = pcount
		pfirst = max(1, plast - 2 * zone)
	
	return offset, limit, dict(current=page, count=pcount, 
							range=range(pfirst, plast+1))
	
	
def dict_update_filled_params(d, **kwargs):
	d.update(dict([(key, value) for key, value in kwargs.iteritems() if value is not None]))
			
		