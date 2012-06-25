from flask import Blueprint, g, abort, request, redirect, url_for
from heymoose.resource import users

blueprint = Blueprint('cabinetcpa', __name__, url_prefix='/cabinet', 
					static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():
	if not g.user:
		return redirect(url_for('site.login', back=request.url))
	g.user = users.get_by_id(g.user.id)
	if not g.user.is_affiliate and not g.user.is_advertiser:
		return redirect(url_for('site.gateway'))
	
	# Do not allow blocked users to create and manage orders or apps 
	if g.user.blocked and 'cabinet/profile' not in request.url:
		return redirect(url_for('.profile'))
	
	# For form validation
	if request.method == 'POST' and request.files:
		request.form = request.form.copy()
		request.form.update(request.files)


# Import all views in blueprint for registering in app's url map
from views import base, offers, stats, profile