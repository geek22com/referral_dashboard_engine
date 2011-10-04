# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms
from heymoose.thirdparty.facebook.mongo.data import Gifts

@frontend.route('/add_gift', methods=['POST', 'GET'])
@admin_only
def add_gift():
	if request.method == 'POST':
		gift_form = forms.GiftAddForm(request.form)
		if gift_form.validate():
			gift = Gifts(title=gift_form.gifttitle.data,
						price=int(gift_form.giftprice.data),
						desc=gift_form.giftdesc.data,
						path=gift_form.giftpath.data)
			gift.save()
		else:
			abort(404)
		return redirect(url_for('user_cabinet', username=g.user.nickname))
	return render_template('add-gift.html', params=g.params)
