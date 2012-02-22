from flask import Blueprint, g, abort, request, redirect, url_for

blueprint = Blueprint('cabinet', __name__, url_prefix='/cabinet', 
					static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():	
	if not g.user:
		return redirect(url_for('site.login', back=request.url))
	
	# Do not allow blocked or unconfirmed users to create and manage orders or apps 
	if (g.user.blocked or not g.user.confirmed) and 'cabinet/info' not in request.url:
		return redirect(url_for('.info'))
	
	# For form validation
	if request.method == 'POST' and request.files:
		request.form = request.form.copy()
		request.form.update(request.files)


# Import all views in blueprint for registering in app's url map
import views