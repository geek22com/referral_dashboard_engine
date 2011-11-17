# -*- coding: utf-8 -*-
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from heymoose.utils.decorators import auth_only
from heymoose.utils.decorators import admin_only
from heymoose.utils.workers import app_logger
from heymoose.views.frontend import frontend
from heymoose.views.work import *
from heymoose.db.models import FeedBack
from heymoose.db.models import Contact
from heymoose.db.models import Captcha
from heymoose.db.actions import captcha
import heymoose.forms.forms as forms

def feedback_form_template(form_params=None, error=None):
	feedback_form = forms.FeedBackForm()
	if form_params:
		feedback_form.feedback_email.data = form_params['feedback_email']
		feedback_form.feedback_comment.data = form_params['feedback_comment']

	g.params['feedbackform'] = feedback_form
	g.params['feedback_captcha'] = captcha.get_random()
	return render_template('index.html', params=g.params)

def contact_form_template(form_params=None, error=None):
    contact_form = forms.ContactForm()
    if form_params:
        contact_form.name.data = form_params['name']
        contact_form.email.data = form_params['email']
        contact_form.phone.data = form_params['phone']
        contact_form.comment.data = form_params['comment']
    g.params['contactform'] = contact_form
    g.params['contact_captcha'] = captcha.get_random()
    return render_template('new_contacts.html', params=g.params)


@frontend.route('/about')
def about():
	return render_template('new_about.html', params=g.params)


@frontend.route('/contacts', methods=['GET', 'POST'])
def contacts():
    contact_form = forms.ContactForm(request.form)
    if request.method == 'POST' and contact_form.validate():
        if captcha.check_captcha(request.form['captcha_id'], contact_form.captcha_answer.data) is None:
            flash_form_errors([['Каптча введена не верно']], 'contactinfoerror')
        else:
            contact = Contact(name= contact_form.name.data,
                                email = contact_form.email.data,
                                phone = contact_form.phone.data,
                                desc = contact_form.comment.data)
            contact.save()
            flash_form_errors([["Спасибо, мы обязательно с вами свяжемся"]], 'contactinfoerror')
            return redirect(url_for('contacts'))
    flash_form_errors(contact_form.errors.values(), 'contactinfoerror')
    return contact_form_template(request.form)


@frontend.route('/to_advertiser')
def to_advertiser():
        return render_template('new-to-advertiser.html', params=g.params)
@frontend.route('/to_partner')
def to_partner():
        return render_template('new-to-partner.html', params=g.params)



#@frontend.route('/feedback', methods=['GET', 'POST'])
#def feedback():
#	feedback_form = forms.FeedBackForm(request.form)
#	if request.method == 'POST' and feedback_form.validate():
#		if captcha.check_captcha(request.form['captcha_id'], feedback_form.feedback_captcha_answer.data) is None:
#			flash_form_errors([['Каптча введена не верно']], 'feedbackerror')
#		else:
#			feedback = FeedBack(email = feedback_form.feedback_email.data,
#							body = feedback_form.feedback_comment.data)
#			feedback.save()
#			flash_form_errors([["Спасибо, мы обязательно учтем ваш отзыв"]], 'feedbackerror')
#			return redirect(url_for('feedback'))
#
#	flash_form_errors(feedback_form.errors.values(), 'feedbackerror')
#	return feedback_form_template(request.form)
