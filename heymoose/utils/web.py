# -*- coding: utf-8 -*-
from werkzeug.exceptions import HTTPException
from werkzeug.routing import RoutingException
from werkzeug.utils import redirect


class RedirectException(HTTPException, RoutingException):
	code = 302

	def __init__(self, new_url):
		RoutingException.__init__(self, new_url)
		self.new_url = new_url

	def get_response(self, environ):
		return redirect(self.new_url)


def force_redirect(new_url):
	raise RedirectException(new_url)
