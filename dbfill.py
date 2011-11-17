from werkzeug import generate_password_hash
from heymoose.core import actions
from heymoose.core.actions import api
import time

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
	
	# Create and enable orders for customers
	orders = []
	genders = (None, True, False)
	for i in range(orders_per_customer):
		for customer in customers:
			id = actions.orders.add_order(
				userId=customer.id,
				title='order {0}-{1}'.format(customer.id, i),
				body='http://ya.ru',
				balance=i*10 + customer.id*10 + 10,
				cpa=i + customer.id + 1,
				desc='The best order from {0} number {1}'.format(customer.nickname, i),
				image_data='aaaa',
				male=genders[i % 3],
				minAge=i + customer.id + 1,
				maxAge=i + customer.id + 15)
			actions.orders.enable_order(id)
			orders.append(actions.orders.get_order(id))
			
	# Create apps for developers
	apps = []
	for i in range(apps_per_developer):
		for developer in developers:
			id = actions.apps.add_app(
				user_id=developer.id,
				callback='http://google.com',
				url='http://google.com')
			apps.append(actions.apps.get_app(id))
			
	
	
	# Create actions for apps and offers
	platforms = ('VKONTAKTE', 'FACEBOOK', 'ODNOKLASSNIKI')
	for app in apps:
		for order in orders:
			for i in range(actions_per_app_and_order):
				api.do_offer(
					offer_id=order.id,
					app_id=app.id,
					uid=app.id + order.id + i,
					platform=platforms[app.id % 3], # One platform per app!
					secret=app.secret)
	
if __name__ == '__main__':
	fill_db()
