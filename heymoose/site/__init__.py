from flask import Blueprint, g, abort, request
from heymoose.forms import forms


blueprint = Blueprint('site', __name__, url_prefix='', static_folder='static', template_folder='templates')

@blueprint.before_request
def before_request():
	g.login_form = forms.LoginForm()


# Import all views in blueprint for registering in app's url map
import views, feeds