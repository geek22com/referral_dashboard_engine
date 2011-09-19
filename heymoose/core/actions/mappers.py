from heymoose.core.actions.base import get_value, get_attr
from heymoose.core.data import User, App, Order, Action

def role_from_xml(role_element):
	return role_element.text

def app_from_xml(app_element):
	return App(id=get_attr(app_element, 'id', int),
				secret=get_value(app_element, 'secret'),
				user_id=get_value(app_element, 'user-id', int))

def order_from_xml(order_element):
	return Order(id=get_attr(order_element, 'id', int),
				title=get_value(order_element, 'title'),
				balance=get_value(order_element, 'balance', float),
				body=get_value(order_element, 'body'),
				cpa=get_value(order_element, 'cpa', float),
				user_id=get_value(order_element, 'user_id', int))

def user_from_xml(user_element):
	return User(id=get_attr(user_element, 'id', int),
				email=get_value(user_element, 'email'),
				nickname=get_value(user_element, 'nickname'),
				password_hash=get_value(user_element, 'password-hash'),
				apps=map(app_from_xml, user_element.xpath('/user/apps')),
				orders=map(order_from_xml, user_element.xpath('/user/orders/order')),
				roles=map(role_from_xml, user_element.xpath('/user/roles/role')),
				customer_balance=get_value(user_element, 'customer-account', float),
				developer_balance=get_value(user_element, 'developer-account', float))

def action_from_xml(action_element):
	return Action(id=get_attr(action_element, 'id', int),
					performer_id=get_value(action_element, 'performer-id', int),
					offer_id=get_value(action_element, 'offer-id', int),
					done=get_value(action_element, 'done', bool),
					deleted=get_value(action_element, 'deleted', bool),
					creation_time=get_value(action_element, 'creation-time'))


### TESTS START HERE ###
import unittest
from lxml import etree

class MapperTest(unittest.TestCase):
	def test_user_mapper(self):
		xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
			<user id="1">
				<email>email</email>
				<nickname>nick</nickname>
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

