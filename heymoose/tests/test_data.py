# -*- coding: utf-8 -*-
from heymoose.data.models import User
from heymoose.data.enums import Roles, ExtendedRoles, MessengerTypes

xml = '''\
	<user id="5">
		<email>testuser@example.com</email>
		<roles>
			<role>ADMIN</role>
			<role>DEVELOPER</role>
		</roles>
		<customer-account id="123">
			<balance>345</balance>
		</customer-account>
		<orders>
			<order id="1">
				<title>Order 1</title>
			</order>
			<order id="2">
				<title>Order 2</title>
			</order>
			<order />
		</orders>
		<confirmed>t</confirmed>
		<blocked />
	</user>
'''

user = User(xml)

print user.fields
print user.id, user.email, user.roles, user.account, user.orders, user.confirmed, user.blocked
print user.account.id, user.account.balance

for order in user.orders:
	print order.id, order.title, order.user

user.email = u'aaa@bbb.ru'
user.email = u'bbb@ccc.ru'
print user._dirty


print Roles.values()
print Roles.values('name')
print Roles.tuples('name', 'shortname')
print MessengerTypes.tuples('name')
print ExtendedRoles.values()
print ExtendedRoles.values('name')