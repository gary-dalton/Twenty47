#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  signals.py
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
from flask import flash, template_rendered
from twenty47 import app, subscription_updated, subscription_pending, sns_error, dispatch_created
from twenty47 import utils, debug
from flask.ext.security.signals import user_confirmed
from flask.ext.login import user_logged_in

"""
Subscribe to signals
"""
@template_rendered.connect_via(app)
def when_template_rendered(sender, template, context, **extra):
    # Not used
    pass

@subscription_updated.connect_via(app)
def when_subscription_updated(sender, user):
    # Works
    utils.update_user_subscriptions()
    
@subscription_pending.connect_via(app)
def when_subscription_pending(sender, user):
    # Works
    approve_url = utils.get_activation_link(str(user.id), 'subscriptionapprove')
    deny_url = utils.get_activation_link(str(user.id), 'subscriptiondeny')
    email_to = utils.get_users_with_role(role_name='SubMan', list_of='email')
    utils.send_mail('Subscription Pending', email_to, 'subscription_enabled', user=user, approve_url=approve_url, deny_url=deny_url)
    debug("Subscription Pending email sent")

@sns_error.connect_via(app)
def when_sns_error(app, func, e):
    # Works
    utils.send_mail('SNS Error', ['gary@gruffgoat.com'], 'sns_error', func=func, e=e)

@user_confirmed.connect_via(app)
def when_user_confirmed(sender, user):
    # Works
    approve_grant_url = utils.get_activation_link(str(user.id), 'makeuser')
    approve_url = utils.get_activation_link(str(user.id), 'makeregistered')
    deny_url = utils.get_activation_link(str(user.id), 'deactivate')
    context = {
            "user": user,
            "approve_grant_url": approve_grant_url,
            "approve_url": approve_url,
            "deny_url": deny_url
        }
    email_to = utils.get_users_with_role(role_name='Manager', list_of='email')
    utils.send_mail('New User Confirmed', email_to, 'user_confirmed', **context)
    debug("User Confirmed email sent")
    
@dispatch_created.connect_via(app)
def when_dispatch_created(sender, dispatch):
    splitter = dispatch.incidentType.split("::")
    dispatch.incidentType = splitter[1]
    splitter = dispatch.unitsImpacted.split("::")
    dispatch.unitsImpacted = splitter[1]
    splitter = dispatch.assistanceRequested.split("::")
    dispatch.assistanceRequested = splitter[1]
    
    context = {
            "dispatch": dispatch,
        }
    utils.put_sns_email_message('New Dispatch', 'dispatch_created', **context)
    utils.send_mail('New Dispatch', ['gary@gruffgoat.com'], 'dispatch_created', **context)

