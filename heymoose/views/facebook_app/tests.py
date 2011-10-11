import json
import sys, os
import md5
import re
from BeautifulSoup import BeautifulSoup
from heymoose.thirdparty.facebook.mongo.performers import get_available_gifts

cmd_folder = os.path.dirname(os.path.abspath("/home/kshilov/PycharmProjects/frontend/frontend-1.0/heymoose"))
if cmd_folder not in sys.path:
	sys.path.insert(0, cmd_folder)
import __builtin__
__builtin__.DEBUG_CONFIG="/home/kshilov/PycharmProjects/frontend/frontend-1.0/config_debug.py"

# ALl import MUST start here
from flask.helpers import url_for
import time
import signal
from heymoose import app, config
from heymoose.core.rest import get, post
from heymoose.core.actions import users, apps
from heymoose.thirdparty.facebook.mongo import performers, invites
from heymoose.thirdparty.facebook.mongo.data import Performer, AccountAction
from heymoose.thirdparty.facebook.actions.oauth import get_app_access_token
from heymoose.core.actions.users import get_user_by_email
from heymoose.thirdparty.facebook.actions import invitations

PERFORMER_1_ID = "11111111111"
PERFORMER_2_ID = "22222222222"
PERFORMER_3_ID = "33333333333"
PERFORMER_REAL_IVAN_IVANOV = "100002951584387"
DEBUG_PORT = 8989

#See inside werkzeug to know how app.run() work, and why it starts another process
if os.environ.get('WERKZEUG_RUN_MAIN', ''):
	app.run(port=DEBUG_PORT, debug=True)

import unittest
if __name__ == "__main__":
	print "__main__ started" + str(os.getpid())
	#start separate thread with debug_app
	pid = os.fork()
	if not pid:
		mypid = os.getpid()
		os.setpgid(mypid, 0)

		print "Child process started"
		app.run(port=DEBUG_PORT, debug=True)
		print "Die"
		exit(0)

	try:
		print "Parent process started"
		time.sleep(2)
		print "Child pid={0}".format(pid)

		class FacebookTest(unittest.TestCase):
			def test_create_performer(self):
				performer1 = performers.get_performer(PERFORMER_1_ID)
				if not performer1:
					performer1 = Performer(user_id=PERFORMER_1_ID,
								oauth_token="qweqweqweqwe",
								expires="123456",
								fullname="Kirill Shilov",
								firstname="Kirill",
								lastname="Shilov")
					performer1.save()

				performer2 = performers.get_performer(PERFORMER_2_ID)
				if not performer2:
					performer2 = Performer(user_id=PERFORMER_2_ID,
									oauth_token="qweqweqweqwe",
									expires="123456",
									fullname="Natalya Loshkina",
									firstname="Natalya",
									lastname="Loshkina")
					performer2.save()

				self.assertEqual(PERFORMER_1_ID, performers.get_performer(PERFORMER_1_ID).user_id)
				self.assertEqual(PERFORMER_2_ID, performers.get_performer(PERFORMER_2_ID).user_id)

			def test_facebook_do_offer(self):
				performer1 = performers.get_performer(PERFORMER_1_ID)
				expect_count = performer1.offers_count + 1
				with app.test_client() as c:
					rv = c.get('/set_cookie/{0}'.format(PERFORMER_1_ID))
					rv = c.post('/facebook_do_offer', follow_redirects=False)

				performer1 = performers.get_performer(PERFORMER_1_ID)
				self.assertEqual(performer1.offers_count, expect_count)

#			def test_do_offer_backend(self):
#				heymoose_developer = users.get_user_by_email('ks.shilov@gmail.com', full=True)
#				current_app = apps.active_apps(heymoose_developer.apps)[0] if heymoose_developer else None
#				self.assertFalse(not heymoose_developer)
#				self.assertFalse(not current_app)
#
#				heymoose_app_id = current_app.id
#				m = md5.md5()
#				m.update(unicode(current_app.id) + unicode(current_app.secret))
#				heymoose_app_sig = m.hexdigest()
#
#				performer1 = performers.get_performer(PERFORMER_1_ID)
#				self.assertFalse(not performer1)
#
#
#				path = '/offers'
#				offers = get(path,
#				             params_dict=dict(app=heymoose_app_id,
#											extId=performer1.user_id,
#											sig=heymoose_app_sig),
#				             renderer=lambda x: x)
#				self.assertFalse(not offers)
#

#				offers_soup = BeautifulSoup(offers)
#				forms = offers_soup.findAll('form')
#				actions = map(lambda next: next.get('action').replace('/rest_api',''), forms)
#				self.assertFalse(not actions)
#				print actions

#				try:
#					post(path=actions[0],params_dict=dict(platform="FACEBOOK",
#														extId=str(performer1.user_id)))
#				except Exception as inst:
#					print inst

#			def test_action_notify(self):
#				performer1_balance = performers.get_performer_balance(PERFORMER_1_ID)
#				expect_balance = performer1_balance + 10
#				with app.test_client() as c:
#					rv = c.get('/set_cookie/{0}'.format(PERFORMER_1_ID))
#					rv = c.post('/main_callback/', data=dict(extId=PERFORMER_1_ID,
#															offerId=3,
#															amount=10))
#
#				new_balance = performers.get_performer_balance(PERFORMER_1_ID)
#				self.assertEqual(new_balance, expect_balance)

#			def test_mlm_notify(self):
#				performer1_balance = performers.get_performer_balance(PERFORMER_1_ID)
#				performer2_balance = performers.get_performer_balance(PERFORMER_2_ID)
#
#				performer1_passive_revenue = 2
#				performer2_passive_revenue = -1
#
#				performer1_expect_balance = performer1_balance + performer1_passive_revenue
#				performer2_expect_balance = performer2_balance + performer2_passive_revenue
#
#				heymoose_developer = users.get_user_by_email('ks.shilov@gmail.com', full=True)
#				current_app = apps.active_apps(heymoose_developer.apps)[0] if heymoose_developer else None
#				self.assertFalse(not heymoose_developer)
#				self.assertFalse(not current_app)
#
#				heymoose_app_id = current_app.id
#
#				items = [{"extId":PERFORMER_1_ID,"passiveRevenue":performer1_passive_revenue},{"extId":PERFORMER_2_ID,"passiveRevenue":performer2_passive_revenue}]
#				with app.test_client() as c:
#					rv = c.post('/main_callback/', data=dict(items=json.dumps(items),
#															appId=heymoose_app_id,
#															fromTime="2011-10-08T01:58:00.000+04:00",
#															toTime="2011-10-09T01:58:00.000+04:00"))
#
#				performer1_new_balance = performers.get_performer_balance(PERFORMER_1_ID)
#				performer2_new_balance = performers.get_performer_balance(PERFORMER_2_ID)
#				self.assertEqual(performer1_new_balance, performer1_expect_balance)
#				self.assertEqual(performer2_new_balance, performer2_expect_balance)
#
#			def test_send_gift(self):
#				from_id = PERFORMER_2_ID
#				to_id = PERFORMER_1_ID
#
#				from_performer_balance = performers.get_performer_balance(from_id)
#				gifts = performers.get_available_gifts(from_id)
#				self.assertFalse(not gifts)
#				map(lambda gift: self.assertFalse(gift.price > from_performer_balance), gifts)
#
#				with app.test_client() as c:
#					rv = c.get('/set_cookie/{0}'.format(from_id))
#					rv = c.post('/facebook_send_gift', data=dict(to_id=to_id,
#																gift_id=str(gifts[0].mongo_id)),
#					                                    follow_redirects=True)
#					print rv.headers
#					self.assertEqual(rv.status_code, 200)
#
#
#			def test_gift(self):
#				performer1 = performers.get_performer(PERFORMER_1_ID)
#				performer1_balance = performers.get_performer_balance(performer1.user_id)
#
#				gifts = performers.get_available_gifts(performer1.user_id)
#				self.assertFalse(not gifts)
#				map(lambda gift: self.assertFalse(gift.price > performer1_balance), gifts)
#
#				with app.test_client() as c:
#					print dir(c)
#					rv = c.get('/set_cookie/{0}'.format(PERFORMER_1_ID))
#					rv = c.post('/facebook_send_gift', data=dict(to_id=PERFORMER_2_ID,
#																gift_id=str(gifts[0].mongo_id)),
#					                                    follow_redirects=True)
#					print rv.headers
#					self.assertEqual(rv.status_code, 200)
#
#				performer1_after_send_gift_balance = performers.get_performer_balance(PERFORMER_1_ID)
#				performer1_after_send_gift_expected_balance = performer1_balance - gifts[0].price
#				self.assertEqual(performer1_after_send_gift_balance, performer1_after_send_gift_expected_balance)
#
#				new_gifts = performers.get_available_gifts(performer1.user_id)
#				self.assertFalse(not new_gifts)
#				map(lambda gift: self.assertFalse(gift.price > performer1_after_send_gift_balance), new_gifts)
#
#				gift_action = AccountAction.query.filter(AccountAction.performer_id == PERFORMER_1_ID,
#														AccountAction.recipient_id == PERFORMER_2_ID,
#														AccountAction.operation == 'gift').all()
#				self.assertNotEqual(gift_action, None)
#
#
#			def test_performer_gifts(self):
#				gifts = performers.get_gifts(PERFORMER_1_ID)
#				print len(gifts)
#				print gifts[0]["gift"].data
#
#			def test_performer_stat(self):
#				with app.test_client() as c:
#					rv = c.get('/set_cookie/{0}'.format(PERFORMER_1_ID))
#					rv = c.post('/facebook_tmpl/stat')
#
#					self.assertEqual(rv.status_code, 200)
#					print rv.data
#
#
#			def test_app_access_token(self):
#				token = get_app_access_token()
#				self.assertNotEqual(token, None)
#
#			def test_invitations(self):
#				invite_from = None
#				if performers.is_performer_new(PERFORMER_REAL_IVAN_IVANOV):
#					invite_from = invitations.check_invite(PERFORMER_REAL_IVAN_IVANOV)
#				self.assertNotEqual(invite_from, None)
#
#				performer = Performer(dirty = False,
#										oauth_token = '',
#										expires = '',
#										user_id = PERFORMER_REAL_IVAN_IVANOV,
#										fullname = "Ivan Ivanov",
#										firstname = "Ivan",
#										lastname = "Ivanov")
#				performer.save()
#
#				if invite_from:
#					heymoose_developer = get_user_by_email(config.get('APP_EMAIL'), full=True)
#					current_app = apps.active_apps(heymoose_developer.apps)[0] if heymoose_developer else None
#					invitations.confirm_invite(performer.user_id, invite_from, current_app.id)
#
#
#				cur_invites = invites.get_invites(performer.user_id)
#				self.assertNotEqual(invites, None)
#
#				found_invite = None
#				for invite in cur_invites:
#					if invite.to_id == PERFORMER_REAL_IVAN_IVANOV:
#						found_invite = invite
#						break
#
#				self.assertNotEqual(found_invite, None)
#				print found_invite.from_id
#				print found_invite.to_id
#				print found_invite.date
#
#			def test_backend_invitations(self):
#				to_id = PERFORMER_3_ID
#				from_id = PERFORMER_1_ID
#				heymoose_developer = get_user_by_email(config.get('APP_EMAIL'), full=True)
#				current_app = apps.active_apps(heymoose_developer.apps)[0] if heymoose_developer else None
#				invitations.confirm_invite(to_id, from_id, current_app.id)
#
#			def test_collect_invitaions(self):
#				cur_invites = invites.get_invites(PERFORMER_REAL_IVAN_IVANOV)
#				self.assertNotEqual(invites, None)
#
#				found_invite = None
#				for invite in cur_invites:
#					if invite.to_id == PERFORMER_REAL_IVAN_IVANOV:
#						found_invite = invite
#						break
#
#				self.assertNotEqual(found_invite, None)
#				print found_invite.from_id
#				print found_invite.to_id
#				print found_invite.date
#
		unittest.main()

	finally:
		# app.run() start another process inside, so to kill all
		# this process we should send kill signal to gid (man kill)
		raw_input("Press Enter to continue...")
		os.kill(-1*pid, signal.SIGTERM)
		os.waitpid(pid, 0)
