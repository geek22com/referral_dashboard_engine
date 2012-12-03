# -*- coding: utf-8 -*-
from flask import request, redirect, flash
from heymoose import app, signals, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.data.enums import AdminStates


@bp.route('/placements/<int:id>/block/')
def placements_info_block(id):
	placement = rc.placements.get_by_id(id)
	placement.admin_state = AdminStates.BLOCKED
	placement.admin_comment = None
	rc.placements.moderate(placement)
	signals.placement_moderated.send(app, placement=placement)
	flash(u'Размещение заблокировано', 'success')
	return redirect(request.args['back'])


@bp.route('/placements/<int:id>/unblock/')
def placements_info_unblock(id):
	placement = rc.placements.get_by_id(id)
	placement.admin_state = AdminStates.APPROVED
	placement.admin_comment = None
	rc.placements.moderate(placement)
	signals.placement_moderated.send(app, placement=placement)
	flash(u'Размещение разблокировано', 'success')
	return redirect(request.args['back'])
