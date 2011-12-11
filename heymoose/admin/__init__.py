from flask import Blueprint, g, abort
from heymoose.db.models import Contact

blueprint = Blueprint('admin', __name__, url_prefix='/admin', 
					static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():
	if g.user is None or not g.user.is_admin():
		abort(403)
		
	g.feedback_unread = Contact.query.filter(Contact.read == False).count()

# Import all views in blueprint for registering in app's url map
import views