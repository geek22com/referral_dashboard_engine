from flask import Blueprint, g, abort, request, redirect, url_for
from heymoose.data.mongo.models import Contact, AdminPermissions

blueprint = Blueprint('admin', __name__, url_prefix='/admin', 
					static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():
	if not g.user:
		return redirect(url_for('site.login', back=request.url))
	elif not g.user.is_admin:
		return redirect(url_for('cabinetcpa.index'))

	# Retreive admin permissions for current user
	g.user.admin_permissions = AdminPermissions.query.get_or_create(user_id=g.user.id)
	
	# For form validation
	if request.method == 'POST' and request.files:
		request.form = request.form.copy()
		request.form.update(request.files)
		
	g.feedback_unread = Contact.query.filter(Contact.read == False).count()

# Import all views in blueprint for registering in app's url map
from views import base, users, offers, stats, site, logs, notifications, finances