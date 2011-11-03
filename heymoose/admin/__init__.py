from flask import Blueprint

blueprint = Blueprint('admin', __name__, url_prefix='/admin', 
					static_folder='static', template_folder='templates')

# Import all views in blueprint for registering in app's url map
import views