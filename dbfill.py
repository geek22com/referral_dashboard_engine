from werkzeug import generate_password_hash
from heymoose.core import actions

def fill_db():
	pw = generate_password_hash('password')
	
	email_admin = 'a@a.ru'
	actions.users.add_user(email_admin, pw, 'admin')
	admin = actions.users.get_user_by_email(email_admin)
	actions.users.add_user_role(admin.id, actions.roles.ADMIN)
	
	email_customer = 'c@c.ru'
	actions.users.add_user(email_customer, pw, 'customer')
	customer = actions.users.get_user_by_email(email_customer)
	actions.users.add_user_role(customer.id, actions.roles.CUSTOMER)
	
	email_developer = 'd@d.ru'
	actions.users.add_user(email_developer, pw, 'developer')
	developer = actions.users.get_user_by_email(email_developer)
	actions.users.add_user_role(developer.id, actions.roles.DEVELOPER)
	
	
	actions.users.increase_customer_balance(customer.id, 1000000)
	
	genders = (None, True, False)
	for i in range(100):
		actions.orders.add_order(
			userId=customer.id,
			title='order {0}'.format(i),
			body='http://ya.ru',
			balance=i * 10 + 10,
			cpa=i + 1,
			desc='The best order from customer number {0}'.format(i),
			image_data='aaaa',
			male=genders[i % 3],
			minAge=i + 1,
			maxAge=i + 15)


if __name__ == '__main__':
	fill_db()