# -*- coding: utf-8 -*-
from flask import Blueprint, g, abort, request, redirect, url_for, flash
from heymoose.data.mongo.models import Contact

blueprint = Blueprint('admin', __name__, url_prefix='/admin', 
					static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():
	if not g.user:
		return redirect(url_for('site.login', back=request.url))
	elif not g.user.is_admin:
		return redirect(url_for('cabinetcpa.index'))

	if g.user.blocked:
		flash(u'Ваша учетная запись администратора заблокирована.', 'danger')
		return redirect(url_for('site.logout'))
	
	# For form validation
	if request.method == 'POST' and request.files:
		request.form = request.form.copy()
		request.form.update(request.files)
		
	g.feedback_unread = Contact.query.filter(Contact.read == False).count()

# Import all views in blueprint for registering in app's url map
from views import base, users, offers, sites, placements, fraud, stats, site, logs, notifications, finances