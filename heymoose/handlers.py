from flask import session, g
from heymoose import app
# Do not remove unused imports here!
from heymoose.core.actions import users, orders, bannersizes, apps, actions, performers, shows, api


@app.before_request
def before_request():
    g.user = None
    g.performer = None
    g.params = {}
    
    if 'user_id' in session:
        g.user = users.get_user_by_id(session['user_id'], full=True)

    #if 'performer_id' in session:
    #    g.performer = performers.get_performer(session['performer_id'])

