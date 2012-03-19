# -*- coding: utf-8 -*-
import argparse, urllib, urllib2, cookielib, time, traceback
from datetime import datetime

LOGIN_URL = 'https://passport.yandex.ru/passport?mode=auth'

class LoginError(ValueError): pass


def build_opener():
	cj = cookielib.CookieJar()
	return urllib2.build_opener(urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cj))

def login(opener, username, password):
	data = {
		#'display': 'page',
		#'from': 'passport',
		#'idkey': '16Y1332106510InI8T0GLS',
		'login': username,
		'passwd': password,
		#'retpath': 'http://moikrug.ru/',
		#'timestamp': time.mktime(datetime.now().timetuple())
	}
	print urllib.urlencode(data.items())
	result = opener.open(LOGIN_URL, urllib.urlencode(data.items()))
	print result.info()
	#print result.read()
	if 'b-login-error' in result.read():
		raise LoginError('Bad username or password')

def search(opener):
	print opener.open('http://moikrug.ru').read()

def invite(args):
	opener = build_opener()
	login(opener, args.username, args.password)
	#search(opener)
	print 'INVITE'

def emails(args):
	login(args.username, args.password)
	print 'EMAILS'


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=u'Parser and inviter for Moi Krug (http://moikrug.ru/).')
	subparsers = parser.add_subparsers(help='action you want parser to perform')
	parser.add_argument('username', help='account username in Moi Krug')
	parser.add_argument('password', help='account password in Moi Krug')
	
	parser_invite = subparsers.add_parser('invite', help='find users by search term and invite them to first Circle')
	parser_invite.add_argument('search', help='search term')
	parser_invite.add_argument('message', help='message to be sent to invited users')
	parser_invite.set_defaults(func=invite)
	
	parser_emails = subparsers.add_parser('emails', help='list emails of users in first Circle')
	parser_emails.set_defaults(func=emails)
	
	args = parser.parse_args()
	try:
		args.func(args)
	except:
		print traceback.format_exc().splitlines()[-1]