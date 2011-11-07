from flask import abort
from restkit.errors import ResourceError

def do_or_abort(func, *args, **kwargs):
	try:
		return func(*args, **kwargs)
	except ResourceError as e:
		abort(e.status_int)
	except:
		abort(500)
		