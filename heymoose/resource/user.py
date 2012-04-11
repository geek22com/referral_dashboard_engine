from backend import BackendResource, ResourceNotFound, extractor
from heymoose.data.models import User

class UserResource(BackendResource):
	base_path = '/users'
	
	extractor = extractor().alias(
		firstName='first_name',
		lastName='last_name',
		sourceUrl='source_url',
		messengerType='messenger_type',
		messengerUid='messenger_uid',
		passwordHash='password_hash'
	)
	
	def get_by_id(self, id, **kwargs):
		return self.path(id).get(**kwargs).as_obj(User)
	
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
			required='email passwordHash firstName lastName'.split(),
			optional='organization phone sourceUrl messengerType messengerUid referrer'.split()
		)
		self.post(**params)
	
	def update(self, user):
		params = self.extractor.extract(user,
			updated='''email passwordHash firstName lastName organization phone
				sourceUrl messengerType messengerUid confirmed blocked'''.split()
		)
		self.path(user.id).put(**params)
	
	def change_email(self, id, email):
		self.path(id).path('email').put(email=email)
	
	def add_to_customer_account(self, id, amount):
		self.path(id).path('customer-account').put(amount=amount)

	def confirm(self, id):
		self.path(id).path('confirmed').put()
	
	def block(self, id):
		self.path(id).path('blocked').put()
	
	def unblock(self, id):
		self.path(id).path('blocked').delete()
	
	def list(self, **kwargs):
		return self.path('list').get(**kwargs).as_objlist(User)
	
	def count(self, **kwargs):
		return self.path('list').path('count').get(**kwargs).as_xmlvalue(int)
