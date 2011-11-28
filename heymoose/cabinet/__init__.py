from flask import Blueprint, g, abort, request

blueprint = Blueprint('cabinet', __name__, url_prefix='/cabinet', 
					static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():
	# For form validation
	if request.method == 'POST' and request.files:
		request.form = request.form.copy()
		request.form.update(request.files)
		
	if g.user is None:
		abort(403)

# Import all views in blueprint for registering in app's url map
import views