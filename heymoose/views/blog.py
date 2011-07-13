# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.models import Category
from heymoose.db.models import Blog

def set_prev_next(pagenum):
	nextpage = 0 if not pagenum else int(pagenum) + 1
	prevpage = 0 if (not pagenum or int(pagenum) <= 0) else int(pagenum) - 1
	g.params['nextpage'] = nextpage
	g.params['prevpage'] = prevpage
	return prevpage, nextpage


@frontend.route('/blog/<pagenum>')
def blog(pagenum=None):
	if int(pagenum) < 0:
		abort(404)

	categories = Category.load_categories()
	if categories:
		g.params['categories'] = categories

	offset = 0
	if pagenum and int(pagenum) > 0:
		offset = int(pagenum) * 10

	blogs = Blog.load_blogs(offset = offset)
	if blogs:
		g.params['blogs'] = blogs
	set_prev_next(pagenum)
	return render_template('cabinet-blog.html', params=g.params)

@frontend.route('/show_category/<category_id>/<pagenum>')
def show_category(category_id=None, pagenum=None):
	if not category_id:
		return redirect(url_for('blog'), pagenum=0)

	offset = 0
	if pagenum and int(pagenum) > 0:
		offset = int(pagenum) * 10

	blogs = Blog.load_blogs_by_category(category_id=category_id, offset=offset)
	if blogs:
		g.params['blogs'] = blogs

	categories = Category.load_categories()
	if categories:
		g.params['categories'] = categories

	category = Category.load_category(category_id)
	if category:
		g.params['category'] = category

	set_prev_next(pagenum)
	return render_template('category-blog.html', params=g.params)

@frontend.route('/add_blog', methods=['POST', 'GET'])
@admin_only
def add_blog():
	categories = Category.load_categories()
	if categories:
		g.params['categories'] = categories

	if request.method == 'POST':
		file = None
		try:
			file = request.files['bloglist']
		except:
			file = None

		if file:
			g.params['blogtext'] = file.stream.read().decode('utf8')
		elif request.form['blogname']:
			blog = Blog(request.form['blogcategory'],
					  request.form['blogname'],
					  request.form['blogtext'],
					  request.form['imagepath'])
			blog.save_new()
			return redirect(url_for('blog', pagenum=0))
	return render_template('add-blog.html', params=g.params)

@frontend.route('/add_category', methods=['POST', 'GET'])
@admin_only
def add_category():
	categories = Category.load_categories()
	if categories:
		g.params['categories'] = categories

	if request.method == 'POST':
		if request.form['categorytitle']:
			category = Category(request.form['categorytitle'])
			category.save_new()
			return redirect(url_for('blog', pagenum=0))
	return render_template('add-category.html', params=g.params)


@frontend.route('/import_blog')
@admin_only
def import_blog():
	return render_template('blog-import.html', params=g.params)

