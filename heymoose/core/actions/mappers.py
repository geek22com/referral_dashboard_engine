from heymoose.core.actions.base import get_value, get_attr, get_child
from heymoose.core.data import User, App, Order, BannerSize, Banner, City, Action, Performer, \
	OrderShow, StatCtr, Account, Transaction
from heymoose.utils.convert import datetime_from_api, datetime_from_unixtime, to_bool

def role_from_xml(role_element):
	if role_element is None: return None
	return role_element.text

def referral_from_xml(referral_element):
	if referral_element is None: return None
	return referral_element.text


def app_from_xml(app_element):
	if app_element is None: return None
	return App(id=get_attr(app_element, 'id', int),
				title=get_value(app_element, 'title'),
				secret=get_value(app_element, 'secret'),
				user_id=get_value(app_element, 'user-id', int),
				user=user_from_xml(get_child(app_element, 'user')),
				platform=get_value(app_element, 'platform'),
				callback=get_value(app_element, 'callback'),
                url=get_value(app_element, 'url'),
				deleted=get_value(app_element, 'deleted', bool),
				creation_time=datetime_from_api(get_value(app_element, 'creation-time')))

def order_from_xml(order_element):
	if order_element is None: return None
	return Order(id=get_attr(order_element, 'id', int),
				user=user_from_xml(get_child(order_element, 'user')),
				user_id=get_value(order_element, 'user-id', int),
				cpa=get_value(order_element, 'cpa', float),
				disabled=get_value(order_element, 'disabled', bool),
				paused=get_value(order_element, 'paused', bool),
				creation_time=datetime_from_api(get_value(order_element, 'creation-time')),
				account=account_from_xml(get_child(order_element, 'account')),
				# Common offer fields
				offer_id=get_value(order_element, 'offer-id', int),
				title=get_value(order_element, 'title'),
				url=get_value(order_element, 'url'),
				auto_approve=get_value(order_element, 'auto-approve', bool),
				reentrant=get_value(order_element, 'reentrant', bool),
				type=get_value(order_element, 'type'),
				# Regular offer fields
				description=get_value(order_element, 'description'),
				image=get_value(order_element, 'image'),
				# Banner offer fields
				banners=map(banner_from_xml, order_element.xpath('./banners/banner')),
				# Video offer fields
				video_url=get_value(order_element, 'video-url'),
				# Targeting fields
				male=get_value(order_element, 'male', bool),
				min_age=get_value(order_element, 'min-age', int),
				max_age=get_value(order_element, 'max-age', int),
				min_hour=get_value(order_element, 'min-hour', int),
				max_hour=get_value(order_element, 'max-hour', int),
				city_filter_type=get_value(order_element, 'city-filter-type'),
				cities=map(city_from_xml, order_element.xpath('./cities/city')),
				app_filter_type=get_value(order_element, 'app-filter-type'),
				apps=map(app_from_xml, order_element.xpath('./apps/app')))
	
def banner_size_from_xml(size_element):
	if size_element is None: return None
	return BannerSize(id=get_attr(size_element, 'id', int),
				width=get_value(size_element, 'width', int),
				height=get_value(size_element, 'height', int),
				disabled=get_value(size_element, 'disabled', bool))
	
def banner_from_xml(banner_element):
	if banner_element is None: return None
	return Banner(id=get_attr(banner_element, 'id', int),
				size=banner_size_from_xml(get_child(banner_element, 'banner-size')),
				mime_type=get_value(banner_element, 'mime-type'),
				image=get_value(banner_element, 'image'))
	
def city_from_xml(city_element):
	if city_element is None: return None
	return City(id=get_attr(city_element, 'id', int),
				name=get_value(city_element, 'name'),
				disabled=get_value(city_element, 'disabled', bool))

def user_from_xml(user_element):
	if user_element is None: return None
	return User(id=get_attr(user_element, 'id', int),
				email=get_value(user_element, 'email'),
				password_hash=get_value(user_element, 'password-hash'),
				first_name=get_value(user_element, 'first-name'),
				last_name=get_value(user_element, 'last-name'),
				organization=get_value(user_element, 'organization'),
				phone=get_value(user_element, 'phone'),
				source_url=get_value(user_element, 'source-url'),
				messenger_type=get_value(user_element, 'messenger-type'),
				messenger_uid=get_value(user_element, 'messenger-uid'),
				confirmed=get_value(user_element, 'confirmed', bool),
				blocked=get_value(user_element, 'blocked', bool),
				register_time=datetime_from_api(get_value(user_element, 'register-time')),
				apps=map(app_from_xml, user_element.xpath('./apps/app')),
				orders=map(order_from_xml, user_element.xpath('./orders/order')),
				roles=map(role_from_xml, user_element.xpath('./roles/role')),
				referrer=get_value(user_element, 'referrer', int),
				referrals=map(referral_from_xml, user_element.xpath('./referrals/referral')),
				revenue=get_value(user_element, 'revenue'),
                customer_secret=get_value(user_element, 'customer-secret'),
                customer_account=account_from_xml(get_child(user_element, 'customer-account')),
                developer_account=account_from_xml(get_child(user_element, 'developer-account')))
	
def account_from_xml(account_element):
	if account_element is None: return None
	return Account(id=get_attr(account_element, 'id', int),
				balance=get_value(account_element, 'balance', float),
				allow_negative_balance=get_value(account_element, 'allow-negative-balance', bool))
	
def transaction_from_xml(transaction_element):
	if transaction_element is None: return None
	return Transaction(id=get_attr(transaction_element, 'id', int),
				diff=get_value(transaction_element, 'diff', float),
				balance=get_value(transaction_element, 'balance', float),
				description=get_value(transaction_element, 'description'),
				type=get_value(transaction_element, 'type'),
				creation_time=datetime_from_api(get_value(transaction_element, 'creation-time')),
				end_time=datetime_from_api(get_value(transaction_element, 'end-time')))

def action_from_xml(action_element):
	if action_element is None: return None
	return Action(id=get_attr(action_element, 'id', int),
				performer_id=get_value(action_element, 'performer-id', int),
				performer=performer_from_xml(get_child(action_element, 'performer')),
				offer_id=get_value(action_element, 'offer-id', int),
				order=order_from_xml(get_child(action_element, 'order')),
				app=app_from_xml(get_child(action_element, 'app')),
				done=get_value(action_element, 'done', bool),
				deleted=get_value(action_element, 'deleted', bool),
				creation_time=datetime_from_api(get_value(action_element, 'creation-time')),
				approve_time=datetime_from_api(get_value(action_element, 'approve-time')),
				attempts=get_value(action_element, 'attempts'))
	
def performer_from_xml(performer_element):
	if performer_element is None: return None
	return Performer(id=get_attr(performer_element, 'id', int),
				ext_id=get_value(performer_element, 'ext-id'),
				platform=get_value(performer_element, 'platform'),
				creation_time=datetime_from_api(get_value(performer_element, 'creation-time')),
				inviter=performer_from_xml(get_child(performer_element, 'inviter')),
				male=get_value(performer_element, 'male', bool),
				year=get_value(performer_element, 'year', int),
				city=get_value(performer_element, 'city'))
	
	
def order_show_from_xml(show_element):
	if show_element is None: return None
	return OrderShow(id=get_attr(show_element, 'id', int),
				show_time=datetime_from_api(show_element.text))
	
	
def stat_from_xml(stat_element):
	if stat_element is None: return None
	return StatCtr(id=get_attr(stat_element, 'id', int),
		gender=get_attr(stat_element, 'gender', to_bool),
		year=get_attr(stat_element, 'year', int),
		city=get_attr(stat_element, 'city'),
		shows=get_attr(stat_element, 'shows', int),
		actions=get_attr(stat_element, 'actions', int),
		performers=get_attr(stat_element, 'performers', int),
		ctr=get_attr(stat_element, 'ctr', float),
		time=datetime_from_unixtime(get_attr(stat_element, 'time', float), True)
	)
	
	
def count_from_xml(count_element):
	return int(count_element.text)


### TESTS START HERE ###
import unittest
from lxml import etree

class MapperTest(unittest.TestCase):
	def test_user_mapper(self):
		xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
			<user id="1">
				<email>email</email>
				<first-name>nick</first-name>
				<password-hash>202cb962ac59075b964b07152d234b70</password-hash>
				<customer-account>30.0</customer-account>
				<developer-account>0.0</developer-account>
				<orders>
					<order id="1">
						<title>title</title>
						<balance>20.0</balance>
						<approved>true</approved>
					</order>
					<order id="2">
						<title>title</title>
						<balance>20.0</balance>
						<approved>false</approved>
					</order>
				</orders>
				<app id="1">
					<secret>15e63936-cd75-4cb9-84ff-b0bc49d3e8a7</secret>
				</app>
				<roles>
					<role>DEVELOPER</role>
					<role>CUSTOMER</role>
				</roles>
			</user>
			"""

		user = user_from_xml(etree.fromstring(xml))
		self.assertTrue('DEVELOPER' in user.roles)
		self.assertEqual(user.orders[0].title, 'title')
		self.assertEqual(user.orders[0].balance, 20.0)

	def test_action_mapper(self):
		xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
				<action id="2">
					<performer-id>1</performer-id>
					<offer-id>2</offer-id>
					<done>false</done>
					<deleted>false</deleted>
					<creation-time>13 Sep 2011 19:32:56 GMT</creation-time>
				</action>"""

		action = action_from_xml(etree.fromstring(xml))
		self.assertEqual(action.id, 2)


if __name__ == "__main__":
	unittest.main()

