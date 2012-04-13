from heymoose import app
from restkit import Resource
from restkit.errors import ResourceError, ResourceNotFound #@UnusedImport
from lxml import etree
import urlparse, os


class RequestBuilder(object):
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


class ResponseRenderer(object):
	def __init__(self, response):
		self.response = response
	
	def as_xml(self): return etree.fromstring(self.response)
	def as_xmlvalue(self, vtype): return vtype(self.as_xml().text)
	def as_obj(self, model): return model(self.as_xml())
	def as_str(self): return unicode(self.response)
	def as_int(self): return int(self.response)
	def render(self, fun): return fun(self.response)
	
	def as_objlist(self, model, with_count=False):
		xml = self.as_xml()
		objects = [model(elem) for elem in xml]
		if with_count:
			count = xml.attrib['count']
			return objects, count
		return objects


class ParamsExtractor(object):	
	def __init__(self, aliases=None):
		self.aliases = aliases or {}
	
	def alias(self, **aliases):
		self.aliases.update(aliases)
		return self
	
	def extend(self):
		return ParamsExtractor(self.aliases.copy())
	
	def extract(self, obj, required=[], nonempty=[], optional=[], updated=[]):
		params = {}
		for param in required:
			value, _ = self._extract_param(obj, param)
			if value is None:
				raise ValueError('{0} is required'.format(param))
			params[param] = value
		for param in nonempty:
			value, _ = self._extract_param(obj, param)
			if not value:
				raise ValueError('{0} should not be empty'.format(param))
			params[param] = value
		for param in optional:
			value, _ = self._extract_param(obj, param)
			if value is not None:
				params[param] = value
		for param in updated:
			value, updated = self._extract_param(obj, param)
			if updated:
				# Workarund: RestKit can't pass empty lists
				if value in ( [], (()), {} ): value = u''
				params[param] = value
		return params
	
	def _extract_param(self, obj, param):
		alias = self.aliases.get(param, None) or param
		if hasattr(alias, '__call__'):
			return alias(obj)
		else:
			attr_chain = alias.split('.')
			updated = False
			value = obj
			for attr_name in attr_chain:
				if value is None: break
				updated = value.is_dirty(attr_name)
				value = getattr(value, attr_name, None)
			return value, updated


def extractor():
	return ParamsExtractor()


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
		return RequestBuilder(self, part)
	
	def loggable_dict(self, d):
		if d is None: return None
		result = {}
		for key, value in d.iteritems():
			if (isinstance(value, str) or isinstance(value, unicode)) and len(value) > 100:
				value = unicode(value)
				result[key] = value[:100] + u'...'
			else:
				result[key] = value
		return result
	
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
			resource=self.__class__.__name__, method=method, url=os.path.join(self.uri, path or ''),
			params=self.loggable_dict(params), payload=self.loggable_dict(payload)
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
		return ResponseRenderer(resp)
		
		
		