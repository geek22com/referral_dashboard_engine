from heymoose import resource

user = resource.users.get_by_id(2)
print user.id, user.email, user.roles, user.developer_account, user.customer_account, user.orders

account = user.developer_account or user.customer_account
print account.id, account.balance