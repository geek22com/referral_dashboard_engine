# -*- coding: utf-8 -*-
from heymoose import app, app_init_basic
from heymoose.commands import manager

@manager.option('-e', '--email', dest='email', default='admin@heymoose.com')
@manager.option('-p', '--pass', dest='password', default='password')
@manager.option('-f', '--first-name', dest='first_name', default=u'Администратор')
@manager.option('-l', '--last-name', dest='last_name', default='HeyMoose')
def createadmin(email, password, first_name, last_name):
	app_init_basic(app)
	
	from heymoose.data.models import User
	from heymoose.data.enums import Roles
	from heymoose.resource import users
	from heymoose.utils.gen import generate_password_hash
	password_hash = generate_password_hash(password)
	user = User(email=email, password_hash=password_hash, first_name=first_name, last_name=last_name)
	users.add(user)
	user = users.get_by_email_safe(email)
	if user:
		users.confirm(user.id)
		users.add_role(user.id, Roles.ADMIN)
	else:
		app.logger.error('Failed to create admin.')
