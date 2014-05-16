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
from flask_wtf import Form
from wtforms import BooleanField, StringField, HiddenField, \
    DateTimeField, SelectField, TextAreaField, PasswordField
from wtforms.validators import Length, InputRequired, Email, EqualTo
from flask.ext.login import current_user
import datetime


class DispatchForm(Form):
    
    operator = HiddenField('Operator',[Length(max=200), InputRequired()], default='operator')
    incidentTime = DateTimeField('Incident Date and Time', [InputRequired()], default=datetime.datetime.now())
    dispatchTime = DateTimeField('Dispatch Date and Time', [InputRequired()], default=datetime.datetime.now())
    streetAddress = StringField('Street Address', [Length(max=200), InputRequired()])
    moreStreetAddress = TextAreaField('More Street Address', [Length(max=255)])
    city = StringField('City', [Length(max=100)])
    state = StringField('State', [Length(max=2), InputRequired()], default='WI')
    postalCode = StringField('Postal Code', [Length(max=20)])
    county = StringField('County', [Length(max=100), InputRequired()])
    incidentType = SelectField('Incident Type')
    unitsImpacted = SelectField('Housing Units Impacted')
    assistanceRequested = SelectField('Type of Assistance Requested')
    responderName = StringField('First Name of DAT Member/DPM Dispatched', [Length(max=200)])
    responderPhone = StringField('Phone Number of DAT Member/DPM Dispatched', [Length(max=100)])


class InstallForm(Form):
    firstName = StringField('First Name',[Length(max=200), InputRequired()], default='Admin')
    lastName = StringField('Last Name', [Length(max=200), InputRequired()], default='Admin')
    email = StringField('Email Address', [Length(max=200), Email(), InputRequired()])
    password = PasswordField('Password', [Length(max=255), InputRequired(), EqualTo('passwordagain', message='Passwords must match')])
    passwordagain = PasswordField('Confirm Password', [Length(max=255), InputRequired()])

