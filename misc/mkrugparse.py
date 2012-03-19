# -*- coding: utf-8 -*-
'''\
Moi Krug parser by Eugeny Slezko.

1. Finds users by keywords, prints their name and URL. Usage:

   $ python mkrugparse.py search "KEYWORDS" USERNAME PASSWORD
   
2. Prints name and email of users in first Circle of specified account. Usage:

   $ python mkrugparse.py emails USERNAME PASSWORD

Needs python >= 2.7 and lxml.
'''

import argparse, urllib, urllib2, cookielib, traceback
from pyquery import PyQuery


class LoginError(ValueError): pass


class MoiKrug(object):
	HEADERS = {
		"User-Agent":"Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Keep-Alive": "115",
		"Connection":"keep-alive"
	}
	URL = 'http://moikrug.ru/'
	LOGIN_URL = 'http://pda-passport.yandex.ru/passport?mode=auth'
	PERSONS_URL = 'http://moikrug.ru/persons/'
	CIRCLE_URL = 'http://moikrug.ru/circles/first/users/'
	
	def __init__(self):
		self.cookie_jar = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
	
	def get(self, url, query=None):
		encoded_query = '?' + urllib.urlencode(query.items()) if query is not None else ''
		req = urllib2.Request(url + encoded_query, headers=self.HEADERS)
		return self.opener.open(req)
	
	def post(self, url, data=None):
		encoded_data = urllib.urlencode(data.items()) if data is not None else None
		req = urllib2.Request(url, encoded_data, self.HEADERS)
		return self.opener.open(req)

	def login(self, username, password):
		data = {
			'login': username,
			'passwd': password,
			'retpath': self.URL,
		}
		html = self.post(self.LOGIN_URL, data).read()
		if 'b-login-error' in html or 'b-error' in html:
			raise LoginError('Bad username or password')
	
	def invite_person(self, url, message):
		html = self.get(url).read()
		d = PyQuery(html)
		fingerprint = d('input[name=fingerprint]').val()
		data = {
			'message[text]': message,
			'fingerprint': fingerprint,
			'send': 'Пригласить в 1-й круг'
		}
		self.post(url, data).read()
	
	def search_page(self, keywords, page):
		query = {
			'keywords': keywords,
			'submitted': 1,
			'perpage': 20,
			'page': page
		}
		html = self.get(self.PERSONS_URL, query).read()
		persons = []
		d = PyQuery(html)
		d('table.search_results tr.item.row').each(lambda i, e: \
			(lambda d: persons.append((
				d('span.person_name a').text().replace(' ', '', 1),
				d('span.person_name a').attr('href'),
				d('a.addUserToFirstCircle').attr('href')
			)))(PyQuery(e))
		)
		for name, href, _ in persons:
			print u'{0:40} {1}'.format(name, href)
		return persons
	
	def search(self, keywords):
		results = True
		page = 1
		while results:
			results = self.search_page(keywords, page)
			page += 1
		print 'No more results.'
	
	def emails(self):
		html = self.get(self.CIRCLE_URL).read()
		persons = []
		d = PyQuery(html)
		d('table.search_results tr.item.row').each(lambda i, e: \
			(lambda d: persons.append((
				d('.name a').text().replace(' ', '', 1),
				d('a.email').text()
			)))(PyQuery(e))
		)
		for name, email in persons:
			print u'{0:40} {1}'.format(name, email)
		print 'No more results.'


def search(args):
	moikrug = MoiKrug()
	moikrug.login(args.username, args.password)
	moikrug.search(args.keywords)

def emails(args):
	moikrug = MoiKrug()
	moikrug.login(args.username, args.password)
	moikrug.emails()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=u'Parser for Moi Krug (http://moikrug.ru/).')
	subparsers = parser.add_subparsers(help='action you want parser to perform')
	parser.add_argument('username', help='account username in Moi Krug')
	parser.add_argument('password', help='account password in Moi Krug')
	
	parser_invite = subparsers.add_parser('search', help='find users by search term and invite them to first Circle')
	parser_invite.add_argument('keywords', help='search terms')
	parser_invite.set_defaults(func=search)
	
	parser_emails = subparsers.add_parser('emails', help='list emails of users in first Circle')
	parser_emails.set_defaults(func=emails)
	
	args = parser.parse_args()
	try:
		args.func(args)
	except:
		print traceback.format_exc().splitlines()[-1]