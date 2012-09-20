from user import UserResource
from account import AccountResource
from withdrawal import WithdrawalResource
from order import OrderResource
from offer import OfferResource
from offergrant import OfferGrantResource
from offerstat import OfferStatResource
from category import CategoryResource
from region import RegionResource
from action import ActionResource
from error import ErrorResource
from public import PublicResource

users = UserResource()
accounts = AccountResource()
withdrawals = WithdrawalResource()
orders = OrderResource()
offers = OfferResource()
offer_grants = OfferGrantResource()
offer_stats = OfferStatResource()
categories = CategoryResource()
regions = RegionResource()
actions = ActionResource()
errors = ErrorResource()
pub = PublicResource()