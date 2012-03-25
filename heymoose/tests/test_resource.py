# -*- coding: utf-8 -*-
from heymoose.resource import UserResource


r = UserResource()

users = r.list(limit=100)
for user in users:
	print user.first_name, user.last_name, user.roles

user = users[1]
user.first_name = u'Петр'
user.last_name = u'Грачев'
r.update(user)

print r.count()