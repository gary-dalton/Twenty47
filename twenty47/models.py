#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  models.py
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
Module models.py documentation
Sets up the models for Twenty47
"""

import datetime
from twenty47 import db, app, subscription_updated
from flask.ext.security import Security, MongoEngineUserDatastore, \
    UserMixin, RoleMixin
from flask_security.forms import RegisterForm, Required, TextField

class Subscriber(db.EmbeddedDocument):
    SUBSCRIBER_STATUS = ("NONE", "DENIED", "PENDING", "APPROVED")
    METHOD = (('None', 'None'), ('Email', 'Email'), ('SMS Phone', 'SMS Phone'), ('Both', 'Both'))
    methods = db.StringField(max_length=100, choices=METHOD, default='None')
    email = db.EmailField()
    email_arn = db.StringField(max_length=250)
    smsPhone = db.StringField(max_length=100)
    sms_arn = db.StringField(max_length=250)
    enabled = db.BooleanField(default=False)
    status = db.StringField(max_length=50, default="NONE", choices=SUBSCRIBER_STATUS)
    
class Role(db.Document, RoleMixin):
    """
    Role class sets up the collection in mongoengine
    """
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now(), required=True)
    modified_at = db.DateTimeField()

class User(db.Document, UserMixin):
    """
    User class sets up the collection in mongoengine
    """
    firstName = db.StringField(max_length=200, required=True)
    lastName = db.StringField(max_length=200, required=True)
    password = db.StringField(max_length=255, required=True)
    email = db.EmailField(required=True, unique=True)
    comments = db.StringField()
    created_at = db.DateTimeField(default=datetime.datetime.now(), required=True)
    modified_at = db.DateTimeField()
    active = db.BooleanField(default=False)
    confirmed_at = db.DateTimeField()
    last_login_at = db.DateTimeField()
    current_login_at = db.DateTimeField()
    last_login_ip = db.StringField(max_length=200)
    current_login_ip = db.StringField(max_length=200)
    login_count = db.IntField()
    roles = db.ListField(db.ReferenceField(Role), default=[])
    subscription = db.EmbeddedDocumentField(Subscriber)

# Setup Flask-Security
class ExtendedRegisterForm(RegisterForm):
    """
    Extends the Registration form to include name information.
    """
    firstName = TextField('First Name', [Required()])
    lastName = TextField('Last Name', [Required()])

class ExtendMEUserDatastore(MongoEngineUserDatastore):
    """
    Extend the MongoEgineUserDatastore to actually carry out some not
    fully mplemented methods.
    """
    
    def activate_user(self, user):
        """Activates a specified user. Returns `True` if a change was made.
        :param user: The user to activate
        """
        if not user.active:
            user.active = True
            self.put(user)
            subscription_updated.send(app, user=user)
            return True
        return False
        
    def deactivate_user(self, user):
        """Deactivates a specified user. Returns `True` if a change was made.
        :param user: The user to deactivate
        """
        if user.active:
            user.active = False
            self.put(user)
            subscription_updated.send(app, user=user)
            return True
        return False
        

user_datastore = ExtendMEUserDatastore(db, User, Role)
security = Security(app, user_datastore,
                confirm_register_form=ExtendedRegisterForm )
                
'''
Setup the mongo data needed for 247
'''
class IncidentType(db.Document):
    name = db.StringField(max_length=200, required=True)
    shortCode = db.StringField(max_length=30, required=True)
    order = db.IntField()
    
class UnitsImpacted(db.Document):
    name = db.StringField(max_length=200, required=True)
    shortCode = db.StringField(max_length=30, required=True)
    order = db.IntField()
    
class AssistanceRequested(db.Document):
    name = db.StringField(max_length=200, required=True)
    shortCode = db.StringField(max_length=30, required=True)
    order = db.IntField()
    
class Dispatch(db.Document):
    operator = db.StringField(max_length=200, required=True)
    incidentTime = db.DateTimeField(default=datetime.datetime.now(), required=True)
    dispatchTime = db.DateTimeField(default=datetime.datetime.now(), required=True)
    streetAddress = db.StringField(max_length=255, required=True)
    moreStreetAddress = db.StringField(max_length=255)
    city = db.StringField(max_length=200)
    state = db.StringField(max_length=2, default='WI', required=True)
    postalCode = db.StringField(max_length=20)
    county = db.StringField(max_length=200, required=True)
    incidentType = db.StringField(max_length=100)
    unitsImpacted = db.StringField(max_length=100)
    assistanceRequested = db.StringField(max_length=100)
    responderName = db.StringField(max_length=200)
    responderPhone = db.StringField(max_length=200)
    created_at = db.DateTimeField(default=datetime.datetime.now(), required=True)

    

'''
# Create a user to test with
@app.before_first_request
def create_user():
    user_datastore.create_user(firstName='Gary', lastName='Dalton', username='garyroot', password='garygoat', email='gary@ggis.biz')
'''

