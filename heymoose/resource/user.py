from backend import BackendResource, ResourceNotFound, extractor
from heymoose.data.models import User

class UserResource(BackendResource):
	base_path = '/users'
	
	extractor = extractor()
	
	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(User)
	
	def get_by_id_safe(self, id, **kwargs):
		try:
			return self.get_by_id(id, **kwargs)
		except ResourceNotFound:
			return None
	
	def get_by_email(self, email, **kwargs):
		return self.get(email=email, **kwargs).as_obj(User)
	
	def get_by_email_safe(self, email, **kwargs):
		try:
			return self.get_by_email(email, **kwargs)
		except ResourceNotFound:
			return None
	
	def add_role(self, id, role):
		return self.path(id).path('roles').post(role=role)
	
	def add(self, user):
		params = self.extractor.extract(user,
			required='email password_hash'.split(),
			optional='organization phone'.split()
		)
		self.post(**params)
	
	def update(self, user):
		params = self.extractor.extract(user,
			updated='''email password_hash first_name last_name organization phone
				source_url messenger_type messenger_uid wmr confirmed blocked'''.split()
		)
		self.path(user.id).put(**params)
	
	def change_email(self, id, email):
		self.path(id).path('email').put(email=email)
	
	def add_to_customer_account(self, id, amount):
		self.path(id).path('customer-account').put(amount=amount)

	def confirm(self, id):
		self.path(id).path('confirmed').put()
	
	def block(self, id, reason):
		self.path(id).path('blocked').put(reason=reason)
	
	def unblock(self, id):
		self.path(id).path('blocked').delete()
	
	def list(self, **kwargs):
		return self.path('list').get(**kwargs).as_objlist(User)
	
	def count(self, **kwargs):
		return self.path('list').path('count').get(**kwargs).as_xmlvalue(int)
