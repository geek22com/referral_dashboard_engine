# -*- coding: utf-8 -*-
from heymoose import app, app_init_assets
from heymoose.commands import manager
from flask.ext.assets import ManageAssets


class AssetsCommand(ManageAssets):
	def run(self, args):
		app_init_assets(app)
		super(AssetsCommand, self).run(args)

manager.add_command('assets', AssetsCommand())
