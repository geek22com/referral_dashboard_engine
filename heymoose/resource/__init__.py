from user import UserResource
from account import AccountResource
from order import OrderResource
from offer import OfferResource
from offergrant import OfferGrantResource
from offerstat import OfferStatResource
from category import CategoryResource

users = UserResource()
accounts = AccountResource()
orders = OrderResource()
offers = OfferResource()
offer_grants = OfferGrantResource()
offer_stats = OfferStatResource()
categories = CategoryResource()