# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.thirdparty.facebook.mongo.data import Gifts
from heymoose import mg
import gridfs
from heymoose.thirdparty.facebook.mongo.data import Gifts
from pymongo import Connection

@frontend.route('/add_gift', methods=['POST', 'GET'])
@admin_only
def add_gift():
	if request.method == 'POST':
		gift_form = forms.GiftAddForm(request.form)
		if gift_form.validate():
			file = request.files['giftimage']
			data = file.stream.read()
			gift = Gifts(title=gift_form.gifttitle.data,
						price=float(gift_form.giftprice.data),
						desc=gift_form.giftdesc.data,
						data=data)
			gift.save()
		else:
			app_logger.debug("add_gift validate error: {0}".format(gift_form.errors))
			abort(404)
		return redirect(url_for('user_cabinet'))
	return render_template('add-gift.html', params=g.params)

@frontend.route('/show_gifts/', methods=['POST', 'GET'])
@frontend.route('/show_gifts/<int:page>/', methods=['POST', 'GET'])
@admin_only
def show_gifts(page=1):
	pagination = Gifts.query.paginate(page=page, per_page=5)
	g.params['pagination'] = pagination
	return render_template('./gifts/list_all.html', params=g.params)


@frontend.route('/gift_data/<string:id>/', methods=['POST', 'GET'])
@admin_only
def gift_data(id):
	gift = Gifts.query.filter(Gifts.mongo_id == id).first()
	if not gift:
		abort(404)
	return gift.data

import unittest
if __name__ == "__main__":
	class GridfsTest(unittest.TestCase):
#		def test_creation(self):
#			db = Connection().gridfs_example
#			fs = gridfs.GridFS(db)
#			f = fs.new_file(filename="hello.txt")
#			f.write("Hello world")
#			f.close()
#		def test_available(self):
#			db = Connection().gridfs_example
#			fs = gridfs.GridFS(db)
#			q = fs.get_version(filename="hello.txt")
#			print q.read()

#		def test_create_gifts(self):
#			gift = Gifts(title="title1",
#						price=14,
#						desc="desc1",
#			            path="path1",
#						data="data1")
#			gift.save()

		def test_load_gifts(self):
			gift = Gifts.query.filter(Gifts.price == 12).first()
			print gift.data
			gift.data = "data2"
			gift.save()
	unittest.main()
