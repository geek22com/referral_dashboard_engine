from heymoose.data.models import User

xml = '''\
	<user id="5">
		<email>testuser@example.com</email>
		<roles>
			<role>ADMIN</role>
			<role>DEVELOPER</role>
		</roles>
		<account id="123">
			<balance>345</balance>
		</account>
		<orders>
			<order id="1">
				<title>Order 1</title>
			</order>
			<order id="2">
				<title>Order 2</title>
			</order>
			<order />
		</orders>
	</user>
'''

user = User(xml)

print user.fields
print user.id, user.email, user.roles, user.account, user.orders
print user.account.id, user.account.balance

for order in user.orders:
	print order.id, order.title

user.email = u'aaa@bbb.ru'
user.email = u'bbb@ccc.ru'
print user._dirty