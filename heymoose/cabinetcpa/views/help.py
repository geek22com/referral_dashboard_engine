# -*- coding: utf-8 -*-
from flask import render_template, abort
from jinja2.exceptions import TemplateNotFound
from heymoose.cabinetcpa import blueprint as bp
from heymoose.cabinetcpa.decorators import affiliate_only


@bp.route('/help/<template>/')
@affiliate_only
def help(template):
	try:
		return render_template('cabinetcpa/help/{0}.html'.format(template))
	except TemplateNotFound:
		abort(404)