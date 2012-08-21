# -*- coding: utf-8 -*-
from flask import g, flash, redirect, url_for, request
from heymoose.db.models import UserInfo
from heymoose.forms import forms
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only
from heymoose.views.decorators import template


@bp.route('/polls/city/', methods=['GET', 'POST'])
@affiliate_only
@template('cabinetcpa/polls/city.html')
def polls_city():
	form = forms.PollCityForm(request.form)
	if request.method == 'POST' and form.validate():
		user_info = UserInfo.query.get_or_create(user_id=g.user.id)
		user_info.city = form.city_select.data or form.city_input.data
		user_info.save()
		flash(u'Спасибо за участие в опросе!', 'success')
		return redirect(url_for('.index'))
	return dict(form=form)