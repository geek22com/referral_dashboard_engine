from flask import render_template, g
from heymoose.admin import blueprint as bp
from heymoose.core import actions

#TODO: make paging in user interface
@bp.route('/')
#@admin_only
def index():
	acs = actions.actions.get_actions(0, 100)
	if acs:
		g.params['actions'] = acs

	ods = actions.orders.get_orders(0, 100)
	if ods:
		g.params['orders'] = ods
		
	return render_template('admin/index.html', params=g.params)