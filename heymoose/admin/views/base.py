# -*- coding: utf-8 -*-
from flask import request, redirect
from heymoose import app
from heymoose.admin import blueprint as bp
from heymoose.data.mongo.models import Contact
from heymoose.views.decorators import template, paginated

CONTACTS_PER_PAGE = app.config.get('CONTACTS_PER_PAGE', 10)

@bp.route('/')
@template('admin/index.html')
def index():
	return dict()

@bp.route('/feedback/', methods=['GET', 'POST'])
@template('admin/feedback.html')
@paginated(CONTACTS_PER_PAGE)
def feedback(offset, limit, **kwargs):
	filters = {
		'contacts': (~(Contact.partner == True), ),
		'partners': (Contact.partner == True, )
	}.get(request.args.get('filter', ''), (()) )
	contacts_query = Contact.query.filter(*filters)
	
	if request.method == 'POST':
		contacts_query.filter(Contact.read == False).set(read=True).multi().execute()
		return redirect(request.url)
	
	count = contacts_query.count()
	contacts = contacts_query.descending(Contact.date).skip(offset).limit(limit).all()
	return dict(contacts=contacts, count=count)