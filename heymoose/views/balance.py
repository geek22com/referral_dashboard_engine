# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only, customer_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger

from heymoose.views.frontend import frontend
import heymoose.forms.forms as forms

############################ Платежная система heymoose.com #####################################################
#	Функции реализующие платежные операции на сайте heymoose.com
#################################################################################################################
