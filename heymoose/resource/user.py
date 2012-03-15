from backend import ModelResource


class UserResource(ModelResource):
	model_name = 'User'
	base_path = '/users'
	
	def get_by_id(self, id, **kwargs):
		return self.model(self.path(id).get(**kwargs))
	
	def get_by_email(self, email, **kwargs):
		return self.model(self.get(**kwargs))
	
	def add_role(self, id, role):
		return self.path(id).path('roles').post(role=role)
	
	def add(self, user):
		params = self.extract_params(user,
			required=(
				'email',
				('password_hash', 'passwordHash'),
				('first_name', 'firstName'),
				('last_name', 'lastName'),
			),
			optional=(
				'organization', 'phone', ('source_url', 'sourceUrl'),
				('messenger_type', 'messengerType'), ('messenger_uid', 'messengerUid'),
				'referrer'
			)
		)
		return self.post(renderer=int, **params)