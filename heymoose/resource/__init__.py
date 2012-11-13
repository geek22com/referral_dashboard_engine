from user import UserResource
from userstat import UserStatResource
from account import AccountResource
from withdrawal import WithdrawalResource
from offer import OfferResource
from offergrant import OfferGrantResource
from offerstat import OfferStatResource
from category import CategoryResource
from region import RegionResource
from banner import BannerResource
from action import ActionResource
from error import ErrorResource
from public import PublicResource
from product import ProductResource
from site import SiteResource

users = UserResource()
user_stats = UserStatResource()
accounts = AccountResource()
withdrawals = WithdrawalResource()
offers = OfferResource()
offer_grants = OfferGrantResource()
offer_stats = OfferStatResource()
categories = CategoryResource()
regions = RegionResource()
banners = BannerResource()
actions = ActionResource()
errors = ErrorResource()
pub = PublicResource()
products = ProductResource()
sites = SiteResource()