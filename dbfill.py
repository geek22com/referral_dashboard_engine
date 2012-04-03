# -*- coding: utf-8 -*-
import os, sys

this_path = os.path.realpath(os.path.dirname(__file__))
project_path = os.path.join(this_path, "heymoose")
config_path = os.path.join(this_path, "config_debug.py")

if project_path not in sys.path:
	sys.path.insert(0, project_path)

os.environ["FRONTEND_SETTINGS_PATH"] = config_path

from heymoose.core import actions
from heymoose.utils.gen import generate_password_hash
from heymoose.data.models import User
from heymoose.data.enums import Roles
from heymoose.resource import users
import time, random

pw = generate_password_hash('password')
email_admin = 'a@a.ru'
email_customer_template = 'c{0}@c.ru'
email_developer_template = 'd{0}@d.ru'
email_advertiser_template = 'ad{0}@ad.ru'
email_affiliate_template = 'af{0}@af.ru'
first_names = (u'Иван', u'Петр', u'Сидор', u'Евгений')
last_names = (u'Иванов', u'Петров', u'Сидоров', u'Ковалев')

customers_count = 10
developers_count = 10
advertisers_count = 3
affiliates_count = 3
orders_per_customer = 10
apps_per_developer = 1
actions_per_app_and_order = 1

def fill_db():
	# Dummy request forces server to regenerate schema
	actions.users.get_users()
	time.sleep(1)
	
	# Create admin
	actions.users.add_user(email_admin, pw, u'Евгений', u'Слезко')
	admin = actions.users.get_user_by_email(email_admin)
	actions.users.confirm_user(admin.id)
	actions.users.add_user_role(admin.id, actions.roles.ADMIN)
	
	# Create customers
	'''customers = []
	for i in range(customers_count):
		email_customer = email_customer_template.format(i)
		actions.users.add_user(email_customer, pw, random.choice(first_names), random.choice(last_names))
		customer = actions.users.get_user_by_email(email_customer)
		actions.users.confirm_user(customer.id)
		actions.users.add_user_role(customer.id, actions.roles.CUSTOMER)
		actions.users.increase_customer_balance(customer.id, 100000 * (i+1))
		customers.append(customer)
		
	# Create developers
	developers = []
	for i in range(developers_count):
		email_developer = email_developer_template.format(i)
		actions.users.add_user(email_developer, pw, random.choice(first_names), random.choice(last_names))
		developer = actions.users.get_user_by_email(email_developer)
		actions.users.confirm_user(developer.id)
		actions.users.add_user_role(developer.id, actions.roles.DEVELOPER)
		developers.append(developer)'''
	
	# Create advertisers
	advertisers = []
	for i in range(advertisers_count):
		email_advertiser = email_advertiser_template.format(i)
		users.add(User(
			email=email_advertiser,
			password_hash=pw,
			first_name=random.choice(first_names),
			last_name=random.choice(last_names)
		))
		advertiser = users.get_by_email(email_advertiser)
		users.confirm(advertiser.id)
		users.add_role(advertiser.id, Roles.ADVERTISER)
		users.add_to_customer_account(advertiser.id, 10000 * (i + 1))
		advertisers.append(advertiser)
	
	# Create affiliates
	affiliates = []
	for i in range(affiliates_count):
		email_affiliate = email_affiliate_template.format(i)
		users.add(User(
			email=email_affiliate,
			password_hash=pw,
			first_name=random.choice(first_names),
			last_name=random.choice(last_names)
		))
		affiliate = users.get_by_email(email_affiliate)
		users.confirm(affiliate.id)
		users.add_role(affiliate.id, Roles.AFFILIATE)
		affiliates.append(affiliate)
		
	'''platforms = ('VKONTAKTE', 'FACEBOOK', 'ODNOKLASSNIKI')
			
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
		
	# Create list of banner sizes
	for i in range(1, 10):
		actions.bannersizes.add_banner_size(i * 100, i * 50)
	banner_sizes = actions.bannersizes.get_banner_sizes()
	
	# Create list of cities
	cities = [u'Москва', u'Санкт-Петербург', u'Харьков', u'Казань', u'Пермь',
			  u'Саратов', u'Нижний Новгород', u'Ростов на Дону']
	for city in cities:
		actions.cities.add_city(city)
	cities = actions.cities.get_cities()
	
	# Create and enable orders for customers
	orders = []
	genders = ('', 'True', 'False')
	cities_filter = ('', 'INCLUSIVE', 'EXCLUSIVE')
	apps_filter = cities_filter
	for i in range(orders_per_customer):
		for customer in customers:
			kwargs = dict(
				user_id=customer.id,
				url='http://ya.ru',
				balance=i*100 + customer.id*10 + 10,
				cpa=i + customer.id + 1,
				male=genders[i % 3],
				min_age=i + customer.id + 1,
				max_age=i + customer.id + 15,
				min_hour=random.randrange(23),
				max_hour=random.randrange(23),
				city_filter_type=cities_filter[i % 3],
				city=[random.choice(cities).id for _j in range(3)],
				app_filter_type=apps_filter[i % 3],
				app=[random.choice(apps).id for _j in range(3)]
			)
			
			if i % 3 == 0:
				kwargs.update(
					title=u'regular order {0}-{1}'.format(customer.id, i),
					description=u'Заказ от пользователя {0} {1} номер {2}'
						.format(customer.first_name, customer.last_name, i),
					image='aGVsbG8h'
				)
				id = actions.orders.add_regular_order(**kwargs)
			elif i % 3 == 1:
				kwargs.update(
					title='banner order {0}-{1}'.format(customer.id, i),
					image='aGVsbG8h',
					banner_mime_type='image/png',
					banner_size=banner_sizes[0].id
				)
				id = actions.orders.add_banner_order(**kwargs)
			else:
				kwargs.update(
					title='video order {0}-{1}'.format(customer.id, i),
					video_url='http://youtube.com'
				)
				id = actions.orders.add_video_order(**kwargs)
			actions.orders.enable_order(id)
			orders.append(actions.orders.get_order(id))
			
	# Create additional banners for banner orders
	for order in orders:
		if order.is_banner():
			sizes = random.sample(banner_sizes[1:], 3)
			for i in range(3):
				actions.orders.add_order_banner(order.id, sizes[i].id, 'image/png', 'aGVsbG8h')
			
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
					city=random.choice(cities).name,
					secret=app.secret)
				
	# Generate some random shows for offers
	for app in apps:
		for performer in performers:
			if app.platform == performer.platform and random.choice([True, False]):
				size = random.choice(banner_sizes)
				filter = '0:3,1:3:{0}x{1},2:3'.format(size.width, size.height)
				actions.api.get_offers(
					app_id=app.id,
					uid=performer.ext_id,
					filter=filter,
					hour=random.randrange(23),
					secret=app.secret)
	'''
	
if __name__ == '__main__':
	fill_db()
