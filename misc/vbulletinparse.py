# -*- coding: utf-8 -*-
'''\
vBulletin forums parser by Eugeny Slezko. Prints list of users in format:

Profile URL | ICQ | Skype

List is sorted by user reputation on forum. Usage:

   $ python vbulletinparse.py --help

Needs python >= 2.7 and lxml.
'''

import argparse, urllib, urllib2, cookielib, traceback, os, re
from pyquery import PyQuery


class VBulletin(object):
	HEADERS = {
		"User-Agent":"Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) Firefox/3.6.6",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Keep-Alive": "115",
		"Connection":"keep-alive"
	}
	
	def __init__(self, url, sort, start_page):
		self.url = url
		self.sort = sort
		self.start_page = start_page
		self.cookie_jar = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie_jar))
	
	def get(self, url, query=None):
		encoded_query = '?' + urllib.urlencode(query.items()) if query is not None else ''
		req = urllib2.Request(url + encoded_query, headers=self.HEADERS)
		return self.opener.open(req)
	
	def post(self, url, data=None):
		encoded_data = urllib.urlencode(data.items()) if data is not None else None
		req = urllib2.Request(url, encoded_data, self.HEADERS)
		return self.opener.open(req, timeout=120)

	def parse_profile(self, url):
		profile_url = os.path.join(self.url, re.sub('s=.*&', '', url))
		html = self.get(profile_url).read()
		d = PyQuery(html)
		icq = d('a.im_txt_link[onclick*="imwindow(\'icq"]').text()
		skype = d('a.im_txt_link[onclick*="imwindow(\'skype"]').text()
		if icq or skype:
			print u'{0:50} {1:16} {2}'.format(profile_url, icq or u'', skype or u'')

	def parse_page(self, page):
		query = {
			'sort' : self.sort,
			'order' : 'desc',
			'pp' : 100,
			'page' : page
		}
		html = self.get(os.path.join(self.url, 'memberlist.php'), query).read()
		profiles = []
		d = PyQuery(html)
		d('td[id*="u"] a').each(lambda i, e: profiles.append(PyQuery(e).attr('href')));
		return profiles

	def parse(self):
		page = self.start_page
		print u'{0:50} {1:16} {2}'.format(u'URL', u'ICQ', u'SKYPE')
		while True:
			print '=== PAGE {0} ==='.format(page)
			profiles = self.parse_page(page)
			for url in profiles:
				self.parse_profile(url)
			page += 1


def parse(args):
	vbulletin = VBulletin(args.url, args.sort, args.page)
	vbulletin.parse()


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description=u'Parser for vBulletin forums.')
	parser.add_argument('url', help='forum url')
	parser.add_argument('-s', '--sort', help='users list sort: posts or reputation', default='posts')
	parser.add_argument('-p', '--page', help='page to start parsing', type=int, default=1)
	parser.set_defaults(func=parse)
	args = parser.parse_args()
	try:
		args.func(args)
	except:
		print traceback.format_exc().splitlines()[-1]