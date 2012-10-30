# -*- coding: utf-8 -*-
from functools import wraps
from jinja2 import Markup


def markup(f):
	@wraps(f)
	def wrapped(*args, **kwargs):
		return Markup(f(*args, **kwargs))
	return wrapped