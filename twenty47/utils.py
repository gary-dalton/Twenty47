#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  utils.py
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
from flask.ext.mail import Message
from twenty47 import app, debug, sns_error
from flask import render_template, flash, abort, redirect, url_for
from flask.ext.mail import Mail
from boto import sns
from twenty47.models import User, Role
from itsdangerous import URLSafeTimedSerializer, BadSignature

mail = Mail(app)
conn = sns.SNSConnection()


def get_all_subscribers():
    get_email_subscribers()
    get_sms_subscribers()
    return

def get_email_subscribers():
    '''
    Returns the subscribers email address and the ARN
    '''
    try:
        subscribers_obj = conn.get_all_subscriptions_by_topic(app.config['DISPATCH_EMAIL_TOPIC'])
        subscribers = dict()
        for subscriber in subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']:
            debug('Email Subscriber %s has the ARN of %s.' % (subscriber['Endpoint'], subscriber['SubscriptionArn']))
            subscribers[subscriber['Endpoint']] = subscriber['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='get_email_subscribers', e=e)
    return subscribers
        
def get_sms_subscribers():
    try:
        subscribers_obj = conn.get_all_subscriptions_by_topic(app.config['DISPATCH_SMS_TOPIC'])
        subscribers = dict()
        for subscriber in subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']:
            subscribers[subscriber['Endpoint']] = subscriber['SubscriptionArn']
            debug('SMS Subscriber %s has the ARN of %s.' % (subscriber['Endpoint'], subscriber['SubscriptionArn']))
    except Exception, e:
        sns_error.send(app, func='get_sms_subscribers', e=e)
    return subscribers

def put_email_subscriber(email):
    try:
        result = conn.subscribe(app.config['DISPATCH_EMAIL_TOPIC'], 'email', email)
        debug('Added email subscriber %s has ARN of %s' % (email, result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']))
        return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='put_email_subscriber', e=e)
    return False
    
def put_sms_subscriber(phone):
    try:
        result = conn.subscribe(DISPATCH_SMS_TOPIC, 'sms', phone)
        debug('Added sms subscriber %s has ARN of %s' % (phone, result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']))
        return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='put_sms_subscriber', e=e)
    return False
    
def del_email_subscriber(arn):
    if arn == "PendingConfirmation":
        debug("Cannot delete subscription because its still Pending")
        return False
    try:
        result = conn.unsubscribe(arn)
        debug("Deleted email subscription of ARN of %s." % (arn))
        return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='del_email_subscriber', e=e)
    return False
    
def del_sms_subscribers(arn):
    if arn == "PendingConfirmation":
        debug("Cannot delete subscription because its still Pending")
        return False
    try:
        result = conn.unsubscribe(arn)
        debug("Deleted SMS subscription of ARN of %s." % (arn))
        return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='del_sms_subscribers', e=e)
    return False
    
def put_sns_sms_message(message):
    """Send an SMS via the Amazon SNS.

    :param message: Plain text message, max length is 160 characters
    """
    try:
        result = conn.publish(topic=app.config['DISPATCH_SMS_TOPIC'], message=message)
        #return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='put_sns_sms_message', e=e)
    return False
    
def put_sns_email_message(subject, template, **context):
    """Send an email via the Amazon SNS.

    :param subject: Email subject
    :param template: The name of the email template
    """
    ctx = ('dispatch/sns', template)
    message = render_template('%s/%s.txt' % ctx, **context)
    
    try:
        result = conn.publish(topic=app.config['DISPATCH_EMAIL_TOPIC'], message=message, subject=subject)
        #return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        sns_error.send(app, func='put_sns_email_message', e=e)
    return False

def update_user_subscriptions(user):
    if not user.subscription:
        debug("Why are we here")
        return False
    else:
        debug(user.subscription.email)
        if user.subscription.email:
            current_subscribers = get_email_subscribers()
            try:
                user.subscription.email_arn = current_subscribers[user.subscription.email]
                if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "Email"):
                    del_email_subscriber(user.subscription.email_arn)
                    user.subscription.email_arn = ''
            except KeyError:
                if user.subscription.status == "APPROVED":
                    if user.subscription.methods == "Both" or user.subscription.methods == "Email":
                        user.subscription.email_arn = put_email_subscriber(user.subscription.email)
                        
        if user.subscription.smsPhone:
            current_subscribers = get_sms_subscribers()
            try:
                user.subscription.sms_arn = current_subscribers['1' + user.subscription.smsPhone]
                if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "SMS Phone"):
                    del_sms_subscribers('1' + user.subscription.smsPhone)
                    user.subscription.sms_arn = ''
            except KeyError:
                if user.subscription.status == "APPROVED":
                    if user.subscription.methods == "Both" or user.subscription.methods == "SMS Phone":
                        user.subscription.sms_arn = put_sms_subscriber('1' + user.subscription.smsPhone)

    user.save()
    return True
    
    
def update_all_user_subscriptions(user):
    
    current_email_subscribers = get_email_subscribers()
    # Create a list of just email addresses
    list_current_email_subscriber = []
    for k, v in current_email_subscribers.iteritems():
        list_current_email_subscriber.append(k)
    debug('Current email subscribers are %s' % (list_current_email_subscriber))
    
    current_sms_subscribers = get_sms_subscribers()
    # Create a list of just phone numbers
    list_current_sms_subscriber = []
    for k, v in current_sms_subscribers.iteritems():
        list_current_sms_subscriber.append(k)
    debug('Current SMS subscribers are %s' % (list_current_sms_subscriber))
    
    users = User.objects(subscription__status="APPROVED")
    needed_email_subscribers = []
    needed_sms_subscribers = []
    # Create lists of needed emails and phone numbers
    for user in users:
        debug(user.subscription.methods)
        if user.subscription.methods == "Both" or user.subscription.methods == "Email":
            needed_email_subscribers.append(user.subscription.email)
            debug("Added " + user.subscription.email)
        if user.subscription.methods == "Both" or user.subscription.methods == "SMS Phone":
            needed_sms_subscribers.append('1' + user.subscription.smsPhone)
    
    debug('Needed email subscribers are %s' % (needed_email_subscribers))
    debug('Needed SMS subscribers are %s' % (needed_sms_subscribers))
    
    # Difference the lists
    add_email_subscribers = list(set(needed_email_subscribers)-set(list_current_email_subscriber))
    remove_email_subscribers = list(set(list_current_email_subscriber)-set(needed_email_subscribers))
    add_sms_subscribers = list(set(needed_sms_subscribers)-set(list_current_sms_subscriber))
    remove_sms_subscribers = list(set(list_current_sms_subscriber)-set(needed_sms_subscribers))
    '''
    # Here we communicate with SNS
    for email_subscriber in add_email_subscribers:
        debug('Add these email subscribers %s' % (email_subscriber))
        user.subscription.email_arn = put_email_subscriber(email_subscriber)
        debug('Added email subscriber %s has ARN of %s' % (email_subscriber, user.subscription.email_arn))
    
    for email_subscriber in remove_email_subscribers:
        debug('Remove these email subscribers %s with ARN %s' % (email_subscriber, current_email_subscribers[email_subscriber]))
        if current_email_subscribers[email_subscriber] != 'PendingConfirmation':
            debug('Can remove this email subscriber %s' % (email_subscriber))
    
    for sms_subscriber in add_sms_subscribers:
        debug('Add these sms subscribers %s' % (sms_subscriber))
        user.subscription.sms_arn = put_sms_subscriber(user)
        flash('Added sms subscriber %s has ARN of %s' % (sms_subscriber, user.subscription.sms_arn))
        
    for sms_subscriber in remove_sms_subscribers:
        if current_sms_subscribers[sms_subscriber] != 'PendingConfirmation':
            debug('Can remove this email subscriber %s' % (sms_subscriber))

    

    '''
    

def send_mail(subject, recipients, template, **context):
    """Send an email via the Flask-Mail extension.

    :param subject: Email subject
    :param recipient: Email recipient
    :param template: The name of the email template
    """
    msg = Message(subject,
                  sender=app.config['SECURITY_EMAIL_SENDER'],
                  recipients=recipients)

    ctx = ('dispatch/email', template)
    msg.body = render_template('%s/%s.txt' % ctx, **context)
    msg.html = render_template('%s/%s.html' % ctx, **context)
    
    mail = Mail(app)
    mail.send(msg)


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = "secret"
        secret_key = app.config['SECRET_KEY']
    return URLSafeTimedSerializer(secret_key)
    
    
def get_activation_link(user_id, action):
    s = get_serializer()
    #payload = s.dumps(user.id, action)
    payload = s.dumps(user_id + "," + action)
    return url_for('admin.remote_admin', payload=payload, _external=True)

def get_users_with_role(role_name=None, list_of=None):
    if role_name is None:
        role_name = "User"
    if list_of is None:
        list_of = "email"

    roles = Role.objects(name=role_name)
    the_list = []
    for role in roles:
        users = User.objects(roles=role)
        for user in users:
            the_list.append(user[list_of])
    return the_list
 
def test_mongo_settings():
    from pymongo import MongoClient
    mc = MongoClient()
    tst_db = mc[app.config['MONGODB_SETTINGS']['DB']]
    try:
        tst_db.authenticate( app.config['MONGODB_SETTINGS']['USERNAME'], password = app.config['MONGODB_SETTINGS']['PASSWORD'] )
        return True
    except Exception, e:
        return e
        
def strip_non_digits(orig_str):
    import string
    orig_str = orig_str.encode('ascii','ignore')
    allchar=string.maketrans('','')
    nodigs=allchar.translate(allchar, string.digits)
    return orig_str.translate(allchar, nodigs)
