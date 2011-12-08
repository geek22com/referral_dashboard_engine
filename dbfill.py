import os, sys

this_path = os.path.realpath(os.path.dirname(__file__))
project_path = os.path.join(this_path, "heymoose")
config_path = os.path.join(this_path, "config_debug.py")

if project_path not in sys.path:
	sys.path.insert(0, project_path)

os.environ["FRONTEND_SETTINGS_PATH"] = config_path

from heymoose.core import actions
from heymoose.utils.gen import generate_password_hash
import time, random

pw = generate_password_hash('password')
email_admin = 'a@a.ru'
email_customer_template = 'c{0}@c.ru'
email_developer_template = 'd{0}@d.ru'
customers_count = 10
developers_count = 10
orders_per_customer = 10
apps_per_developer = 1
actions_per_app_and_order = 1

def fill_db():
	# Dummy request forces server to regenerate schema
	actions.orders.get_orders()
	time.sleep(1)
	
	# Create admin
	actions.users.add_user(email_admin, pw, 'admin')
	admin = actions.users.get_user_by_email(email_admin)
	actions.users.add_user_role(admin.id, actions.roles.ADMIN)
	
	# Create customers
	customers = []
	for i in range(customers_count):
		email_customer = email_customer_template.format(i)
		actions.users.add_user(email_customer, pw, 'customer{0}'.format(i))
		customer = actions.users.get_user_by_email(email_customer)
		actions.users.add_user_role(customer.id, actions.roles.CUSTOMER)
		actions.users.increase_customer_balance(customer.id, 100000 * (i+1))
		customers.append(customer)
		
	# Create developers
	developers = []
	for i in range(developers_count):
		email_developer = email_developer_template.format(i)
		actions.users.add_user(email_developer, pw, 'developer{0}'.format(i))
		developer = actions.users.get_user_by_email(email_developer)
		actions.users.add_user_role(developer.id, actions.roles.DEVELOPER)
		developers.append(developer)
		
	# Create list of banner sizes
	for i in range(1, 10):
		actions.bannersizes.add_banner_size(i * 100, i * 50)
	banner_sizes = actions.bannersizes.get_banner_sizes()
	
	# Create and enable orders for customers
	orders = []
	genders = (None, True, False)
	for i in range(orders_per_customer):
		for customer in customers:
			if i % 3 == 0:
				id = actions.orders.add_regular_order(
						user_id=customer.id,
						title='regular order {0}-{1}'.format(customer.id, i),
						url='http://ya.ru',
						balance=i*100 + customer.id*10 + 10,
						cpa=i + customer.id + 1,
						description='The best order from {0} number {1}'.format(customer.nickname, i),
						image='aaaa',
						male=genders[i % 3],
						min_age=i + customer.id + 1,
						max_age=i + customer.id + 15)
			elif i % 3 == 1:
				id = actions.orders.add_banner_order(
						user_id=customer.id,
						title='banner order {0}-{1}'.format(customer.id, i),
						url='http://ya.ru',
						balance=i*100 + customer.id*10 + 10,
						cpa=i + customer.id + 1,
						image='aaaa',
						banner_size=random.choice(banner_sizes).id,
						male=genders[i % 3],
						min_age=i + customer.id + 1,
						max_age=i + customer.id + 15)
			else:
				id = actions.orders.add_video_order(
						user_id=customer.id,
						title='video order {0}-{1}'.format(customer.id, i),
						url='http://ya.ru',
						balance=i*100 + customer.id*10 + 10,
						cpa=i + customer.id + 1,
						video_url='http://youtube.com',
						male=genders[i % 3],
						min_age=i + customer.id + 1,
						max_age=i + customer.id + 15)
			actions.orders.enable_order(id)
			orders.append(actions.orders.get_order(id))
	
	platforms = ('VKONTAKTE', 'FACEBOOK', 'ODNOKLASSNIKI')
			
	# Create apps for developers
	apps = []
	for i in range(apps_per_developer):
		for developer in developers:
			id = actions.apps.add_app(
				title='app {0}-{1}'.format(developer.id, i),
				user_id=developer.id,
				callback='http://google.com',
				url='http://google.com',
				platform=platforms[i % 3])
			apps.append(actions.apps.get_app(id))
			
	# Create actions for apps and offers
	for app in apps:
		for order in orders:
			for i in range(actions_per_app_and_order):
				actions.api.do_offer(
					offer_id=order.id,
					app_id=app.id,
					uid=app.id + order.id + i,
					platform=platforms[app.id % 3], # One platform per app!
					secret=app.secret)
	
	# Get all created performers
	actions_count = len(apps) * len(orders)
	performers = []
	for i in range(1, actions_count+1):
		try:
			performers.append(actions.performers.get_performer(i))
		except:
			print 'No performer with uid {0}'.format(i)
	
	# Introduce our performers
	for app in apps:
		for performer in performers:
			if app.platform == performer.platform:
				actions.api.introduce_performer(
					app.id,
					uid=performer.ext_id,
					sex=random.choice(['MALE', 'FEMALE']),
					year=random.randint(1970, 2006),
					secret=app.secret)
				
	# Generate some random shows for offers
	for app in apps:
		for performer in performers:
			if app.platform == performer.platform and random.choice([True, False]):
				size = random.choice(banner_sizes)
				filter = '0:3,1:3:{0}x{1},2:3'.format(size.width, size.height)
				actions.api.get_offers(app.id, performer.ext_id, filter, app.secret)

	
if __name__ == '__main__':
	fill_db()
