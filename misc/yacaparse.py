# -*- coding: utf-8 -*-
'''\
Yandex.Catalog parser by Eugeny Slezko.
Prints URLs in specified catalog category.

Usage: python yacaparse.py "http://yaca.yandex.ru/yca/ungrp/cat/Rest/" 5

Last argument (optional) is number of pages to parse (there are 10 URLs per page).
If not specified, all pages are parsed.
'''

from HTMLParser import HTMLParser
import os, sys, urllib2

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs_dict = dict(attrs)
            if attrs_dict.get('class', '') == 'b-result__name':
                href = attrs_dict.get('href', None)
                if href:
                    self.was = True
                    print href


if __name__ == '__main__':
    parser = MyHTMLParser()
    parser.was = False
    url = sys.argv[1]
    pages_cnt = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    
    html = urllib2.urlopen(url).read()
    parser.feed(html)
    
    i = 1
    while not pages_cnt or i < pages_cnt:
        page = os.path.join(url, '{0}.html'.format(i))
        try:
            html = urllib2.urlopen(page).read()
        except:
            break
        parser.was = False
        parser.feed(html)
        if not parser.was:
            break
        i += 1
