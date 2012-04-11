# -*- coding: utf-8 -*-
from flask import render_template, request, g
from heymoose import app, resource as rc
from heymoose.admin import blueprint as bp
from heymoose.db.models import Contact
from heymoose.utils import convert
from heymoose.utils.shortcuts import paginate

@bp.route('/')
def index():
	return render_template('admin/index.html')

@bp.route('/feedback/', methods=['GET', 'POST'])
def feedback():
	filters = {
		'contacts': (~(Contact.partner == True), ),
		'partners': (Contact.partner == True, )
	}.get(request.args.get('filter', ''), (()) )
	
	if request.method == 'POST':
		contacts = Contact.query.filter(Contact.read == False, *filters)
		for contact in contacts: # For some reason set/execute query not working
			contact.read = True
			contact.save()
		g.feedback_unread = Contact.query.filter(Contact.read == False).count()
	
	page = convert.to_int(request.args.get('page'), 1)
	count = Contact.query.filter(*filters).count()
	per_page = app.config.get('ADMIN_CONTACTS_PER_PAGE', 10)
	offset, limit, pages = paginate(page, count, per_page)
	contacts = Contact.query.filter(*filters).descending(Contact.date).skip(offset).limit(limit)
	return render_template('admin/feedback.html', contacts=contacts.all(), pages=pages)