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
		feedback_form.email.data = form_params['email']
		feedback_form.comment.data = form_params['comment']

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
    return render_template('contacts.html', params=g.params)


@frontend.route('/about')
def about():
	return render_template('about.html', params=g.params)


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

@frontend.route('/audience')
def audience():
	return render_template('audience.html', params=g.params)

@frontend.route('/survey_examples')
def survey_examples():
	return render_template('survey-examples.html', params=g.params)

@frontend.route('/to_advertiser')
def to_advertiser():
        return render_template('to-advertiser.html', params=g.params)
@frontend.route('/to_partner')
def to_partner():
        return render_template('to-partner.html', params=g.params)

@frontend.route('/apicode')
def apicode():
	return render_template('apicode.html', params=g.params)

@frontend.route('/facebook_smm')
def facebook_smm():
	return render_template('facebook-smm.html', params=g.params)
@frontend.route('/youtube_smm')
def youtube_smm():
	return render_template('youtube-smm.html', params=g.params)
@frontend.route('/vkontakte_smm')
def vkontakte_smm():
	return render_template('vkontakte-smm.html', params=g.params)
@frontend.route('/popular_smm')
def popular_smm():
	return render_template('popular-smm.html', params=g.params)
@frontend.route('/blog_smm')
def blog_smm():
	return render_template('blog-smm.html', params=g.params)
@frontend.route('/twitter_smm')
def twitter_smm():
	return render_template('twitter-smm.html', params=g.params)
@frontend.route('/vrs_smm')
def vrs_smm():
	return render_template('vrs-smm.html', params=g.params)
@frontend.route('/negativ_smm')
def negativ_smm():
	return render_template('negativ-smm.html', params=g.params)

@frontend.route('/price')
def price():
	return render_template('price.html', params=g.params)




@frontend.route('/feedback', methods=['GET', 'POST'])
def feedback():
	feedback_form = forms.FeedBackForm(request.form)
	if request.method == 'POST' and feedback_form.validate():
		if captcha.check_captcha(request.form['captcha_id'], feedback_form.captcha_answer.data) is None:
			flash_form_errors([['Каптча введена не верно']], 'feedbackerror')
		else:
			feedback = FeedBack(email = feedback_form.email.data,
							body = feedback_form.comment.data)
			feedback.save()
			flash_form_errors([["Спасибо, мы обязательно учтем ваш отзыв"]], 'feedbackerror')
			return redirect(url_for('feedback'))

	flash_form_errors(feedback_form.errors.values(), 'feedbackerror')
	return feedback_form_template(request.form)
