from heymoose import app
from restkit import Resource, BasicAuth
from restkit.errors import ResourceError
from lxml import etree

class MailJet(Resource):
	def __init__(self, uri, key, secret_key, **kwargs):
		auth = BasicAuth(key, secret_key)
		super(MailJet, self).__init__(uri, filters=[auth], **kwargs)
		
		
	def request(self, method, path=None, payload=None, headers=None, params_dict=None, **params):
		# Unify our interface
		if params_dict:
			params.update(params_dict)
			params_dict = None
		
		# So we passed payload in params
		if method != 'GET' and params and payload is None:
			payload = params
			params = {}

		app.logger.debug('MailJet {0}: url={1}/{2} params={3} payload={4}'.format(method,
			self.uri, path, params, payload))
		
		try:
			response = super(MailJet, self).request(method, path, payload, headers, params_dict, **params)
		except ResourceError as e:
			app.logger.error('MailJet request failed ({0}): {1}'.format(e.status_int, e.response.final_url), exc_info=True)	
			raise
		except Exception as e:
			app.logger.error('MailJet request failed: {0}'.format(e.__dict__), exc_info=True)
			raise
		
		resp = response.body_string()
		if response.charset != 'utf8':
			resp = resp.decode('utf8')
			
		return etree.fromstring(resp) if resp else u''


	def lists_add_contact(self, contact, list_id, force=False):
		return self.post('listsAddcontact', contact=contact, id=list_id, force=force)
	
	def lists_remove_contact(self, contact, list_id):
		return self.post('listsRemovecontact', contact=contact, id=list_id)
		

api = MailJet(
	uri = app.config.get('MAILJET_API_URL'),
	key = app.config.get('MAILJET_API_KEY'),
	secret_key = app.config.get('MAILJET_API_SECRET_KEY'),
	timeout = app.config.get('MAILJET_TIMEOUT'),
	max_tries = app.config.get('MAILJET_MAX_TRIES')
)
