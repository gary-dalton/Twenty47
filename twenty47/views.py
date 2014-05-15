#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  views.py
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
Module views.py documentation
FLL handles all needed online forms, etc for FIRST Lego League
"""

from twenty47 import db, app, debug, dispatch_created
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from twenty47.models import Role, User, Dispatch, IncidentType, \
            UnitsImpacted, AssistanceRequested
from twenty47.forms import DispatchForm, InstallForm
from flask.ext.login import current_user
from flask.ext.security import login_required, roles_required, roles_accepted

dispatch = Blueprint('dispatch', __name__, template_folder = 'templates')

class Home(MethodView):
    decorators = [login_required]
    
    def get(self):
        return redirect(self.redirector())
        return render_template('dispatch/index.html')
        
    def redirector(self):
        next_url = url_for('subscriber.create')
        for role in current_user.roles:
            #if role.name == 'Admin':
             #   next_url = url_for('dispatch.dispatch_create')
            if role.name == 'Dispatch':
                next_url = url_for('dispatch.dispatch_create')
        return next_url
        
class DispatchCreate(MethodView):
    decorators = [login_required, roles_required('Dispatch')]
    
    def get_context(self, id=None):

        if id:
            dispatch = Dispatch.objects.get_or_404(id=id)
            if request.method == 'POST':
                form = DispatchForm(request.form, inital=dispatch._data)
            else:
                form = DispatchForm(obj=dispatch)
        else:
            dispatch = Dispatch()
            form = DispatchForm(request.form)
            
        form.incidentType.choices = [[it.shortCode + "::" + it.name, it.name] for it in IncidentType.objects.order_by('order')]
        form.unitsImpacted.choices = [(it.shortCode + "::" + it.name, it.name) for it in UnitsImpacted.objects.order_by('order')]
        form.assistanceRequested.choices = [(it.shortCode + "::" + it.name, it.name) for it in AssistanceRequested.objects.order_by('order')]
        #form_cls.operator.value = current_user.firstName + " " + current_user.lastName

        context = {
            "dispatch": dispatch,
            "form": form,
            "create": id is None
        }
        return context
    
    
    def get(self, id=None):
        context = self.get_context(id)
        return render_template('dispatch/index.html', **context)
        
    def post(self, id):        
        context = self.get_context(id)
        form = context.get('form')
        form.operator.data = current_user.firstName + " " + current_user.lastName
        '''
        for item in form:
            debug(item.data)
        return redirect(url_for('dispatch.dispatch_create'))
        
        '''
        if form.validate():
            dispatch = context.get('dispatch')
            form.populate_obj(dispatch)
            dispatch.save()
            dispatch_created.send(app, dispatch=dispatch)

            return redirect(url_for('dispatch.dispatch_create'))
        return render_template('dispatch/index.html', **context)
    
class Install(MethodView):
    default_broken = {'SECURITY_EMAIL_SENDER': 'email_sender@yourbiz.com',
                    'MONGODB_SETTINGS': {'DB': 'db_name', "USERNAME": 'db_user', 'PASSWORD':'db_pwd'},
                    'MAIL_SERVER': 'SMTP Server',
                    'MAIL_USERNAME': 'smtp email user',
                    'MAIL_PASSWORD': 'smtp email pwd',
                    'DEFAULT_MAIL_SENDER': 'email_sender@yourbiz.com',
                    'DISPATCH_EMAIL_TOPIC': 'arn:aws:sns:us-zone-1:3456345645756756:Dispatch_Email',
                    'DISPATCH_SMS_TOPIC': 'arn:aws:sns:us-zone-1:3456345645756756:Dispatch_SMS',
                    }
                    
    default_dangerous = {'SECRET_KEY': 'thesecretkey',
                    'SECURITY_PASSWORD_SALT': 'some_long_string_for_you_to_change',
                    }
                    
    default_ok = {'CSRF_ENABLED': True}
    
    clsRole = Role
    clsUser = User


    def get_context(self):
        user = User()
        form = InstallForm(request.form)
        context = {
            "user": user,
            "form": form,
        }
        return context
    
    def get(self):
        # If the DB is already initialized, skip install
        if self.clsUser.objects.count() > 0:
            return redirect(url_for('dispatch.index'))
        if self.clsRole.objects.count() > 0:
            context = self.get_context()
            return render_template('dispatch/install.html', **context)
        
        # Not initialized so do the install
        compare_config = self.is_config_default()
        broken = compare_config['broken']
        dangerous = compare_config['dangerous']
        isok = compare_config['ok']
        compare_config['all_ok'] = False
                
        if len(broken) != 0 or len(dangerous) != 0:
            return render_template('dispatch/config_broken.html', **compare_config)
        
        mongo_ok = self.test_mongo_settings()
        if mongo_ok != True:
            flash("Connecting to the database failed because %s. Please verify your database settings" % mongo_ok, 'danger')
            return render_template('dispatch/config_broken.html', **compare_config)
            
        sns_ok = self.test_sns_settings()
        if sns_ok != True:
            flash("Connecting to the SNS failed because %s. Please verify your SNS settings" % sns_ok, 'danger')
            return render_template('dispatch/config_broken.html', **compare_config)
            
        #email_ok = self.test_email_settings()
        # debug
        email_ok = False
        if email_ok != True:
            flash("Sending email failed because %s. Please verify your email settings" % email_ok, 'danger')
            return render_template('dispatch/config_broken.html', **compare_config)
            
        compare_config['all_ok'] = True
        return render_template('dispatch/config_broken.html', **compare_config)
        
            
    
    def is_config_default(self):
        broken_list = []
        dangerous_list = []
        ok_list = []
        debug(app.config['SECURITY_EMAIL_SENDER'])
        for config_key, value in self.default_broken.iteritems():
            try:
                if app.config[config_key] == value:
                    broken_list.append(config_key + " : " + str(app.config[config_key]))
                else:
                    ok_list.append(config_key + " : " + str(app.config[config_key]))
            except KeyError:
                broken_list.append(config_key)
                
        for config_key, value in self.default_dangerous.iteritems():
            try:
                if app.config[config_key] == value:
                    dangerous_list.append(config_key + " : " + str(app.config[config_key]))
                else:
                    ok_list.append(config_key + " : " + str(app.config[config_key]))
            except KeyError:
                dangerous_list.append(config_key)
                
        for config_key, value in self.default_ok.iteritems():
            if app.config[config_key] == value:
                ok_list.append(config_key + " : " + str(app.config[config_key]))
            else:
                dangerous_list.append(config_key + " : " + str(app.config[config_key]))
                
        result = {
            'broken': broken_list,
            'dangerous': dangerous_list,
            'ok': ok_list,
            }
        return(result)
        
    def test_email_settings(self):
        from flask.ext.mail import Mail, Message
        mail = Mail(app)
        msg = Message('Test',
                  sender=app.config['SECURITY_EMAIL_SENDER'],
                  recipients=[app.config['SECURITY_EMAIL_SENDER']],
                  body = "testing")
        try:
            mail.send(msg)
            return True
        except Exception, e:
            return e
            
    def test_mongo_settings(self):
        clsRole = Role
        try:
            roles = clsRole.objects.all()
            return True
        except Exception, e:
            return e
            
    def test_sns_settings(self):
        from boto import sns
        conn = sns.SNSConnection()
        
        msg = ""
        try:
            subscribers_obj = conn.get_all_subscriptions_by_topic(app.config['DISPATCH_EMAIL_TOPIC'])
        except Exception, e:
            msg += "Email topic failed! " + str(e) + "----------"
            
        try:
            subscribers_obj = conn.get_all_subscriptions_by_topic(app.config['DISPATCH_SMS_TOPIC'])
        except Exception, e:
            msg += "SMS topic failed! " + str(e)
            
        if len(msg) > 0:
            return msg
        else:
            return True

class Initialize(MethodView):
    clsRole = Role
    clsIncidentTypes = IncidentType
    clsUnitsImpacted = UnitsImpacted
    clsAssistanceRequested = AssistanceRequested
    
    def post(self):
        start_roles = [{"description" : "Administrative (root) user", "name" : "Admin"},
                { "description" : "User has completed the registration process", "name" : "Registered"},
                {"description" : "Manages users. Receives notification emails of new users and may approve them.", "name" : "Manager"},
                { "description" : "Manages subscriptions. Receives notification emails of new subscriptions and may approve them.", "name" : "SubMan" },
                { "description" : "Only those designated as Dispatch may create Dispatches.", "name" : "Dispatch"}
                ]
        start_it = [{ "name" : "Single Family Fire", "order" : 1, "shortCode" : "SFF" },
                    { "name" : "Multi Family Fire", "order" : 2, "shortCode" : "MFF" },
                    { "name" : "Storm", "order" : 4, "shortCode" : "STM" },
                    { "name" : "Flood", "order" : 5, "shortCode" : "FLD" },
                    { "name" : "Other", "order" : 6, "shortCode" : "OTH" },
                    { "name" : "Non-residential Fire", "shortCode" : "FIR", "order" : 3 },
                    ]
        start_ui = [{ "name" : "1 - 4 Units", "order" : 1, "shortCode" : "4U" },
                    { "name" : "4 - 8 Units", "order" : 2, "shortCode" : "8U" },
                    { "name" : "8 - 16 Units", "order" : 3, "shortCode" : "16U" },
                    { "name" : "More than 16 Units", "order" : 4, "shortCode" : "M16" },
                    ]
        start_ar = [{ "name" : "Individual Assistance", "order" : 1, "shortCode" : "IA" },
                    { "name" : "Canteening", "order" : 2, "shortCode" : "CA" },
                    { "name" : "Larger Scale Response", "order" : 3, "shortCode" : "LG" },
                    ]
                    
        # If the DB is already initialized, skip install
        if self.clsRole.objects.count() > 0:
            return redirect(url_for('dispatch.index'))
        else:
            pass
    

# Register the urls
dispatch.add_url_rule('/', view_func=Home.as_view('index'))
dispatch.add_url_rule('/install', view_func=Install.as_view('install'))
dispatch.add_url_rule('/initialize', view_func=Initialize.as_view('initialize'))
dispatch.add_url_rule('/dispatch/create', defaults={'id': None},view_func=DispatchCreate.as_view('dispatch_create'))
