#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  untitled.py
#  
#  Copyright 2014 Gary Dalton <gary@ggis.biz>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
"""
Module subscriber.py documentation
Handles subscriptions for Twenty47
"""
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from flask.ext.security import login_required, roles_required, script
from flask.ext.login import current_user
from twenty47.models import Subscriber, User
from twenty47 import app, debug, subscription_pending, subscription_updated
from twenty47.utils import put_email_subscriber, put_sms_subscriber, strip_non_digits
from wtforms import validators

subscriber = Blueprint('subscriber', __name__, template_folder='templates')

class Detail(MethodView):

    decorators = [login_required]

    def get_context(self):
        form_cls = model_form(Subscriber,field_args = {
            'smsPhone': {'label': 'SMS Phone Number',
                        'validators' : [validators.Length(min=10, max=10, message='Telephone must be exactly 10 digits.')]},
            'email': {'default': current_user.email},
            })

        #'user': {'default': current_user, 'widget': widgets.HiddenInput()},
        del form_cls.enabled
        del form_cls.status
        del form_cls.email_arn
        del form_cls.sms_arn

        user = User.objects.get_or_404(id=current_user.id)
        if not user.subscription:
            target = Subscriber()
            form = form_cls(request.form)
        else:
            target = user.subscription
            if request.method == 'POST':
                form = form_cls(request.form, inital=user.subscription._data)
            else:
                form = form_cls(obj=target)
        '''        
        if id:
            target = Subscriber.objects.get_or_404(id=current_user.id)
            if request.method == 'POST':
                form = form_cls(request.form, inital=target._data)
            else:
                form = form_cls(obj=target)
        else:
            target = Subscriber()
            form = form_cls(request.form)
        '''

        context = {
            "user": user,
            "target": target,
            "form": form,
            "create": id is None
            }
        return context
        
    def get(self):
        context = self.get_context()
        return render_template('subscriber/detail.html', **context)

    def post(self):        
        context = self.get_context()
        form = context.get('form')
        
        form.smsPhone.data = strip_non_digits(form.smsPhone.data)
      
        if form.validate():
            target = context.get('target')
            form.populate_obj(target)
            user = context.get('user')
            
            current_status = user.subscription.status
            user.subscription = target            
            if current_status == "DENIED":
                flash("Your subscription has been marked as DENIED. Please contact staff to unlock this request.", "danger")
                user.subscription.status = "DENIED"
            elif current_status == "NONE":
                user.subscription.status = "PENDING"
            elif current_status == "APPROVED":
                user.subscription.status = "APPROVED"
       
            if user.save():
                if current_status == "NONE":
                    subscription_pending.send(app, user=context.get('user'))
                elif current_status == "APPROVED":
                    subscription_updated.send(app, user=context.get('user'))
                flash(context.get('user').firstName + " " + context.get('user').lastName + " Subscription Updated", "success")
            return redirect(url_for('subscriber.update'))
            
        return render_template('subscriber/detail.html', **context)
        
class ResendConfirmation(MethodView):
    decorators = [login_required]
    
    def post(self, id):        
        user = User.objects.get_or_404(id=id)
        debug("in class ResendConfirmation")
        
        try:
            if request.form['action'] == "reconfirmEmail":
                if put_email_subscriber(request.form['email']):
                    return "True"
                else:
                    return(app.config['DISPATCH_ERROR_GENERAL'])
            elif request.form['action'] == "reconfirmSMS":
                if put_sms_subscriber('1' + request.form['smsphone']):
                    return "True"
                else:
                    return(app.config['DISPATCH_ERROR_GENERAL'])
                    
        except KeyError, e:
            return(app.config['DISPATCH_ERROR_GENERAL'])
            
            
        
subscriber.add_url_rule('/subscriber/', view_func=Detail.as_view('create'))
subscriber.add_url_rule('/subscriber/', view_func=Detail.as_view('update'))
subscriber.add_url_rule('/subscriber/resend/<id>', view_func=ResendConfirmation.as_view('resend'))
#subscriber.add_url_rule('/subscriber/delete/<action>/<id>', view_func=Remove.as_view('delete'))
