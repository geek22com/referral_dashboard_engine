# -*- coding: utf-8 -*-
from heymoose import app
from datetime import datetime


def ensure_site_info(site):
	site_info = app.mongo.db.site_info.find_one({ 'site_id': site.id })
	if not site_info:
		app.mongo.db.site_info.insert({ 'site_id': site.id, 'comments': [] })


def site_comments_post(site, text, admin=False, private=False):
	ensure_site_info(site)
	now = datetime.now()
	app.mongo.db.site_info.update(
		{ 'site_id': site.id },
		{ '$push': { 'comments': {
			'posted': now,
			'edited': now,
			'admin': admin,
			'private': private,
			'text': text
		} } },
		upsert=True
	)


def site_comments_update(site, id, text):
	ensure_site_info(site)
	app.mongo.db.site_info.update(
		{
			'site_id': site.id,
			'comments.{}.admin'.format(id): True
		},
		{ '$set': {
			'comments.{}.text'.format(id): text,
			'comments.{}.edited'.format(id): datetime.now()
		} }
	)


def site_comments_list(site):
	ensure_site_info(site)
	return app.mongo.db.site_info.find_one({ 'site_id': site.id })['comments']