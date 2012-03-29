from heymoose import app
from flask import request
from math import ceil


def current_page(param='page'):
	try:
		return int(request.args.get(param))
	except:
		return 1

def page_limits(page, per_page):
	return per_page * (page - 1), per_page

def paginate(page, count, per_page):
	pcount = int(ceil(float(count) / per_page)) if per_page > 0 else 0
	if pcount == 0: pcount = 1
	
	# Calculate pages range
	zone = app.config.get('PAGES_RANGE', 7)
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
	
	return dict(current=page, count=pcount, range=range(pfirst, plast+1))