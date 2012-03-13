from heymoose import app
from restkit import Resource
from restkit.errors import ResourceError
import urlparse


class BackendResource(Resource):
	base_url = app.config.get('BACKEND_BASE_URL')
	timeout = app.config.get('BACKEND_TIMEOUT')
	max_tries = app.config.get('BACKEND_MAX_TRIES')
	path = None
	
	def __init__(self, **kwargs):
		timeout = kwargs.pop('timeout', None) or self.timeout
		max_tries = kwargs.pop('max_tries', None) or self.max_tries
		path = kwargs.pop('path', None) or self.path
		
		print self.base_url
		uri = urlparse.urljoin(self.base_url, path)
		super(BackendResource, self).__init__(uri, timeout=timeout, max_tries=max_tries, **kwargs)
	
	def request(self, method, path=None, payload=None, headers=None, params_dict=None, **params):
		# Unify our interface
		if params_dict:
			params.update(params_dict)
			params_dict = None
		
		# So we passed payload in params
		if method != 'GET' and params and payload is None:
			payload = params
			params = {}

		app.logger.debug('{resource} {method}: url={url} params={params} payload={payload}'.format(
			resource=self.__class__.__name__, method=method, url=urlparse.urljoin(self.uri, path),
			params=params, payload=payload
		))
		
		try:
			response = super(BackendResource, self).request(method, path, payload, headers, params_dict, **params)
		except ResourceError as e:
			app.logger.error('{resource} request failed ({status}): {url}'.format(
				resource=self.__class__.__name__,
				status=e.status_int,
				url=e.response.final_url), exc_info=True)
			raise
		except Exception as e:
			app.logger.error('{resource} request failed: {dict}'.format(
				resource=self.__class__.__name__,
				dict=e.__dict__), exc_info=True)
			raise
		
		resp = response.body_string()
		if response.charset != 'utf8':
			resp = resp.decode('utf8')
		return resp