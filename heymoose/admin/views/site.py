# -*- coding: utf-8 -*-
from flask import render_template, request, flash, redirect, url_for
from heymoose.data.mongo.models import NewsItem
from heymoose.forms import forms
from heymoose.utils.pagination import current_page, page_limits, paginate
from heymoose.admin import blueprint as bp
from datetime import datetime


@bp.route('/news/')
def news_list():
	page = current_page()
	per_page = 10
	offset, limit = page_limits(page, per_page)
	news = NewsItem.query.descending(NewsItem.date).skip(offset).limit(limit)
	count = NewsItem.query.count()
	pages = paginate(page, count, per_page)
	return render_template('admin/site/news-list.html', news=news.all(), pages=pages)

@bp.route('/news/new', methods=['GET', 'POST'])
def news_new():
	form = forms.NewsItemForm(request.form, date=datetime.now())
	if request.method == 'POST' and form.validate():
		newsitem = NewsItem()
		form.populate_obj(newsitem)
		newsitem.save()
		flash(u'Новость успешно добавлена', 'success')
		return redirect(url_for('.news_edit', id=newsitem.mongo_id))
	return render_template('admin/site/news-new.html', form=form)

@bp.route('/news/<id>', methods=['GET', 'POST'])
def news_edit(id):
	newsitem = NewsItem.query.get(id)
	form = forms.NewsItemForm(request.form, obj=newsitem)
	if request.method == 'POST' and form.validate():
		form.populate_obj(newsitem)
		newsitem.save()
		flash(u'Новость успешно обновлена', 'success')
		return redirect(request.url)
	return render_template('admin/site/news-edit.html', newsitem=newsitem, form=form)

