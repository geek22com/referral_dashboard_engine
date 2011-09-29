# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.db.actions.categories import load_categories, load_category
from heymoose.db.actions.blogs import load_blog_by_id, load_blogs, load_blogs_by_category
from heymoose.db.models import Blog, Category

def set_prev_next(pagenum):
	nextpage = 0 if not pagenum else int(pagenum) + 1
	prevpage = 0 if (not pagenum or int(pagenum) <= 0) else int(pagenum) - 1
	g.params['nextpage'] = nextpage
	g.params['prevpage'] = prevpage
	return prevpage, nextpage


@frontend.route('/blog_body/<blog_id>')
def blog_body(blog_id=None):
	if not blog_id:
		abort(404)

	categories = load_categories()
	if categories:
		g.params['categories'] = categories

	blog = load_blog_by_id(b_id=blog_id)
	if blog:
		g.params['blog'] = blog
	else:
		abort(404)
	return render_template('current-blog.html', params=g.params)


@frontend.route('/blog/<pagenum>')
def blog(pagenum=None):
	if int(pagenum) < 0:
		abort(404)

	categories = load_categories()
	if categories:
		g.params['categories'] = categories

	offset = 0
	if pagenum and int(pagenum) > 0:
		offset = int(pagenum) * 10

	blogs = load_blogs()
	if blogs:
		g.params['blogs'] = blogs
	set_prev_next(pagenum)
	return render_template('cabinet-blog.html', params=g.params)

@frontend.route('/show_category/<category_id>/<pagenum>')
def show_category(category_id=None, pagenum=None):
	if not category_id:
		return redirect(url_for('blog'), pagenum=0)

	print "FFFFFFFFFFFFf"
	print category_id
	
	offset = 0
	if pagenum and int(pagenum) > 0:
		offset = int(pagenum) * 10

	blogs = load_blogs_by_category(category_id=category_id)
	if blogs:
		g.params['blogs'] = blogs

	categories = load_categories()
	if categories:
		g.params['categories'] = categories

	category = load_category(category_id)
	if category:
		g.params['category'] = category

	set_prev_next(pagenum)
	return render_template('cabinet-blog.html', params=g.params)

@frontend.route('/edit_blog/<blog_id>', methods=['POST', 'GET'])
@admin_only
def edit_blog(blog_id=None):
	if not blog_id:
		abort(404)

	categories = load_categories()
	if categories:
		g.params['categories'] = categories

	blog = load_blog_by_id(blog_id=blog_id)
	if not blog:
		return "No such blog"
	g.params['blog_id'] = blog.mongo_id
	if request.method == 'POST':
		if request.form['blogname']:
			blog.category_id = int(request.form['blogcategory'])
			blog.title = request.form['blogname']
			blog.annotation = request.form['annotation']
			blog.body = request.form['blogtext']
			blog.save()
			return redirect(url_for('blog', pagenum=0))
	else:
		g.params['title'] = blog.title
		g.params['category'] = blog.category_id
		g.params['annotation'] = blog.annotation
		g.params['blogtext'] = blog.body

	return render_template('edit-blog.html', params=g.params)


@frontend.route('/add_blog', methods=['POST', 'GET'])
@admin_only
def add_blog():
	categories = load_categories()
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
			blog = Blog(category_id=request.form['blogcategory'],
					  title=request.form['blogname'],
					  body=request.form['blogtext'],
					  annotation=request.form['annotation'],
					  image_path=request.form['imagepath'])
			blog.save()
			return redirect(url_for('blog', pagenum=0))
	return render_template('add-blog.html', params=g.params)

@frontend.route('/add_category', methods=['POST', 'GET'])
@admin_only
def add_category():
	categories = load_categories()
	if categories:
		g.params['categories'] = categories

	if request.method == 'POST':
		if request.form['categorytitle']:
			category = Category(title=request.form['categorytitle'])
			category.save()
			return redirect(url_for('blog', pagenum=0))
	return render_template('add-category.html', params=g.params)


@frontend.route('/import_blog')
@admin_only
def import_blog():
	return render_template('blog-import.html', params=g.params)

