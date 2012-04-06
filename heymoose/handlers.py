from flask import request, session, g
from heymoose import app
# Do not remove unused imports here!
from heymoose.core.actions import users, orders, bannersizes, apps, \
actions, performers, shows, api, cities, stats, accounts, settings


@app.before_request
def before_request():
	g.user = None
	g.config = app.config
	g.params = {}
	
	if 'user_id' in session and '/static' not in request.url and '/upload' not in request.url:
		print '\n'
		g.user = users.get_user_by_id(session['user_id'])

