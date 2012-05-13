# -*- coding: utf-8 -*-
from flask import make_response, url_for
from heymoose.site import blueprint as bp
from heymoose.db.models import NewsItem
from heymoose.feed import PyRSS2Gen
from datetime import datetime


@bp.route('/feed/')
def rss_feed():
	news = NewsItem.query.filter(NewsItem.active == True).descending(NewsItem.date).limit(15).all()
	items = []
	for newsitem in news:
		link = url_for('site.news_item', id=newsitem.mongo_id, _external=True)
		items.append(PyRSS2Gen.RSSItem(
			title = newsitem.title,
			link = link,
			description = newsitem.summary,
			guid = PyRSS2Gen.Guid(link),
			pubDate = newsitem.date 
		))
	rss = PyRSS2Gen.RSS2(
		title = u'Последние новости HeyMoose',
		link = url_for('site.index', _external=True),
		description = u'HeyMoose — партнерская сеть с оплатой за действия.',
		lastBuildDate = news[0].date if news else datetime.now(),
		items = items,
		generator = None,
		docs = None,
		image = PyRSS2Gen.Image(
			url = url_for('static', filename='./img/logo_120x120.png', _external=True),
			link = url_for('site.index', _external=True),
			title = u'HeyMoose',
			width = 120,
			height = 120
		)
	)
	response = make_response(rss.to_xml(encoding='utf-8'))
	response.headers['Content-Type'] = 'application/xml'
	return response
	



