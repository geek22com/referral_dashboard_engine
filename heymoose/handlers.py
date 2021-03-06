from flask import session, g
from heymoose import app
# Do not remove unused imports here!
from heymoose.core.actions import users, orders, bannersizes, apps, \
actions, performers, shows, api, cities, stats, accounts, settings


@app.before_request
def before_request():
	g.user = None
	g.config = app.config
	g.params = {}
	
	if 'user_id' in session:
		g.user = users.get_user_by_id(session['user_id'])

