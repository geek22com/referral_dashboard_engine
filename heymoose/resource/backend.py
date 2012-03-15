from heymoose import app
from heymoose.data.base import registry
from restkit import Resource
from restkit.errors import ResourceError
from lxml import etree
import urlparse


class PathRequest(object):
	def __init__(self, resource, part):
		self.resource = resource
		self.parts = [str(part)]
	
	def path(self, part):
		self.parts.append(str(part))
		return self
	
	def build(self):
		return '/'.join(self.parts)
	
	def get(self, **kwargs): return self.resource.get(self.build(), **kwargs)
	def post(self, **kwargs): return self.resource.post(self.build(), **kwargs)
	def put(self, **kwargs): return self.resource.put(self.build(), **kwargs)
	def delete(self, **kwargs): return self.resource.delete(self.build(), **kwargs)


class BackendResource(Resource):
	base_url = app.config.get('BACKEND_BASE_URL')
	timeout = app.config.get('BACKEND_TIMEOUT')
	max_tries = app.config.get('BACKEND_MAX_TRIES')
	base_path = None
	
	def __init__(self, **kwargs):
		timeout = kwargs.pop('timeout', None) or self.timeout
		max_tries = kwargs.pop('max_tries', None) or self.max_tries
		base_path = kwargs.pop('base_path', None) or self.base_path
		
		uri = urlparse.urljoin(self.base_url, base_path)
		super(BackendResource, self).__init__(uri, timeout=timeout, max_tries=max_tries, **kwargs)
		
	def path(self, part):
		return PathRequest(self, part)
	
	def request(self, method, path=None, payload=None, headers=None, params_dict=None,
			renderer=etree.fromstring, **params):
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
		return renderer(resp)


class ModelResource(BackendResource):
	model_name = None
	
	@property
	def model(self):
		if getattr(self, '_model', None) is None:
			self._model = registry.get_model(self.model_name)
		return self._model
	
	def apply_mapping(self, mapping, params):
		return dict(((mapping[name] if name in mapping else name), value) for name, value in params.iteritems())
	
	def extract_params(self, obj, required=[], optional=[]):
		params = dict()
		for param in required:
			name, value = self._extract_param(obj, param)
			if value is None:
				raise ValueError('{0} is required'.format(name))
			params[name] = value
		for param in optional:
			name, value = self._extract_param(obj, param)
			if value is not None:
				params[name] = value
		return params
	
	def _extract_param(self, obj, param):
		if isinstance(param, tuple):
			attr_name, param_name = param
		else:
			attr_name = param_name = param
		return param_name, getattr(obj, attr_name)
		
		
		