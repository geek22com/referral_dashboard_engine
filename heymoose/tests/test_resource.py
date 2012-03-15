from heymoose.data.models import User, Order

user = User.resource.get_by_id(2)
print user.id, user.email, user.roles, user.developer_account, user.customer_account, user.orders

account = user.developer_account or user.customer_account
print account.id, account.balance

order = Order.resource.get_by_id(1)
print order.values()
print order.user.values()
print order.stats.values()
print order.type.name

from heymoose.forms.forms import OfferForm

form = OfferForm()
print form.suboffers