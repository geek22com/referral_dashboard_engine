from flask import g, session, request
from heymoose import app
from heymoose.resource import users

@app.before_request
def before_request():
	g.user = None
	g.config = app.config
	g.params = {}
	
	if 'user_id' in session and '/static' not in request.url and '/upload' not in request.url:
		print '\n'
		g.user = users.get_by_id(int(session['user_id']))