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
Module utils.py documentation
A variety of utilities used by Twenty47. These are mostly used
to interact with AWS through boto though some other utilities
are provided.
"""
import sys
from flask.ext.mail import Message
from twenty47 import app, debug, sns_error
from flask import render_template, flash, abort, redirect, url_for
from flask.ext.mail import Mail
from boto import sns
from twenty47.models import User, Role
from itsdangerous import URLSafeTimedSerializer, BadSignature

mail = Mail(app)
conn = sns.SNSConnection()

def put_subscriber(topic, method, endpoint, conn=conn):
    '''
    Returns False or the subscription ARN:
    {'SubscribeResponse': {'SubscribeResult': {'SubscriptionArn': 'arn:aws:sns:us-east-1:123456789012:Dispatch_Email:2a9f687f-2313-411f-88c8-4cce9b29c53b'}, 'ResponseMetadata': {'RequestId': 'a8763b99-33a7-11df-a9b7-05d48da6f042'}}}
    Tested
    '''
    try:
        result = conn.subscribe(topic, method, endpoint)
        debug('Added %s subscriber %s has ARN of %s' % (method, endpoint, result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']))
        return result['SubscribeResponse']['SubscribeResult']['SubscriptionArn']
    except Exception, e:
        return
        sns_error.send(app, func='put_email_subscriber', e=e)
    return False
    
def get_one_subscriber(topic, endpoint, nexttoken=None, conn=conn):
    '''
    Returns False or the subscription data:
    {'Owner': '796928799269', 'Endpoint': 'gary@gruffgoat.com', 'Protocol': 'email', 'TopicArn': 'arn:aws:sns:us-east-1:796928799269:Dispatch_Email', 'SubscriptionArn': 'arn:aws:sns:us-east-1:796928799269:Dispatch_Email:784fe2e3-f495-4c63-85e2-2306c2b400df'}
    Tested
    '''
    try:
        subscribers_obj = conn.get_all_subscriptions_by_topic(topic, nexttoken)
        for subscriber in subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']:
            if subscriber['Endpoint'] == endpoint:
                return subscriber
        if subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['NextToken'] is None:
            return False
        else:
            nexttoken = subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['NextToken']
            return get_one_subscriber(topic, endpoint, nexttoken, conn)
    except Exception, e:
        return ('Error: %s' % (e))
        sns_error.send(app, func='get_one_subscriber', e=e)
    return False
    
def del_subscriber(arn, conn=conn):
    if arn == "PendingConfirmation":
        debug("Cannot delete subscription because its still Pending")
        return False
    try:
        result = conn.unsubscribe(arn)
        debug("Deleted subscription of ARN of %s." % (arn))
        return True
    except Exception, e:
        return ('Error: %s' % (e))
        sns_error.send(app, func='del_subscriber', e=e)
    return False
    
def put_email_subscriber(email, conn=conn):
    return(put_subscriber(app.config['DISPATCH_EMAIL_TOPIC'], 'email', email, conn))
    
def put_sms_subscriber(phone, conn=conn):
    return(put_subscriber(app.config['DISPATCH_SMS_TOPIC'], 'sms', phone, conn))

def get_topic_subscribers(topic, nexttoken=None, subscribers=None, conn=conn):
    '''
    Returns a dictionary of the subscribers' endpoints and the ARNs
    '''
    if subscribers is None:
        subscribers = {}
    try:
        subscribers_obj = conn.get_all_subscriptions_by_topic(topic, nexttoken)
        nexttoken = subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['NextToken']
        for subscriber in subscribers_obj['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']:
            subscribers[subscriber['Endpoint']] = subscriber['SubscriptionArn']
        if nexttoken is None:
            return subscribers
        else:
            return(get_topic_subscribers(topic, nexttoken, subscribers, conn))
    except Exception, e:
        return ('Error: %s' % (e))
        sns_error.send(app, func='get_email_subscribers', e=e)
    return subscribers
    
def get_all_subscribers(conn=conn):
    subscribers = get_email_subscribers(conn=conn)
    subscribers.update(get_sms_subscribers(conn=conn))
    return(subscribers)

def get_email_subscribers(conn=conn):
    return (get_topic_subscribers(app.config['DISPATCH_EMAIL_TOPIC'], nexttoken=None, subscribers=None, conn=conn))
        
def get_sms_subscribers(conn=conn):
    return (get_topic_subscribers(app.config['DISPATCH_SMS_TOPIC'], nexttoken=None, subscribers=None, conn=conn))
    
def del_email_subscriber(arn, conn=conn):
    return del_subscriber(arn, conn=conn)
    
def del_sms_subscriber(arn, conn=conn):
    return del_subscriber(arn, conn=conn)

def put_sns_message(topic, message, subject=None, conn=conn):
    """Send message via Amazon SNS.

    :param message: Plain text message
    """
    try:
        result = conn.publish(topic=topic, message=message)
        return result
    except Exception, e:
        return ('Error: %s' % (e))
        sns_error.send(app, func='put_sns_sms_message', e=e)
    return False
    
def put_sns_sms_message(message, conn=conn):
    """Send an SMS.

    :param message: Plain text message, max length is 160 characters
    """
    try:
        result = conn.publish(topic=app.config['DISPATCH_SMS_TOPIC'], message=message)
        return result
    except Exception, e:
        return ('Error: %s' % (e))
        sns_error.send(app, func='put_sns_email_message', e=e)
    return False
    
    return put_sns_message(app.config['DISPATCH_SMS_TOPIC'], message[:150])
    
    
def put_sns_email_message(subject, template, conn=conn, **context):
    """Send an email via the Amazon SNS.

    :param subject: Email subject
    :param template: The name of the email template
    """
    ctx = ('dispatch/sns', template)
    message = render_template('%s/%s.txt' % ctx, **context)
    #return put_sns_message(app.config['DISPATCH_EMAIL_TOPIC'], message=message, subject=subject)
    
    try:
        result = conn.publish(topic=app.config['DISPATCH_EMAIL_TOPIC'], message=message, subject=subject)
        return result
    except Exception, e:
        return ('Error: %s' % (e))
        sns_error.send(app, func='put_sns_email_message', e=e)
    return False



def update_user_subscriptions(user):
    debug("In utils.update_user_subscriptions")
    if not user.subscription:
        debug("Why are we here")
        return False
    else:
        debug(user.subscription.email)
        debug(user.subscription.smsPhone)
        current_email_subscribers = get_email_subscribers()
        current_sms_subscribers = get_sms_subscribers()
        pending_or_emtpy = ['', 'PendingConfirmation', 'pending confirmation']
        
        if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "Email"):
            # Get the best version of the ARN
            #if  user.subscription.email_arn == '' or user.subscription.email_arn == 'PendingConfirmation':
            if user.subscription.email_arn in pending_or_emtpy:
                try:
                    user.subscription.email_arn = current_email_subscribers[user.subscription.email]
                except KeyError:
                    user.subscription.email_arn = ''
            elif user.subscription.email_arn not in current_email_subscribers.values():
                user.subscription.email_arn = ''
            # Delete if there is an ARN
            #if  user.subscription.email_arn != '' or user.subscription.email_arn != 'PendingConfirmation':
            if user.subscription.email_arn not in pending_or_emtpy:
                debug("Going to delete %s" % user.subscription.email)
                if del_email_subscriber(user.subscription.email_arn) is not False:
                    user.subscription.email_arn = ''
                    
        if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "SMS Phone"):
            # Get the best version of the ARN
            #if  user.subscription.sms_arn == '' or user.subscription.sms_arn == 'PendingConfirmation':
            if user.subscription.sms_arn in pending_or_emtpy:
                try:
                    user.subscription.sms_arn = current_sms_subscribers['1' + user.subscription.smsPhone]
                except KeyError:
                    user.subscription.sms_arn = ''
            elif user.subscription.sms_arn not in current_sms_subscribers.values():
                user.subscription.sms_arn = ''
            # Delete if there is an ARN
            #if  user.subscription.sms_arn != '' or user.subscription.sms_arn != 'PendingConfirmation':
            if user.subscription.sms_arn not in pending_or_emtpy:
                debug("Going to delete %s" % user.subscription.smsPhone)
                if del_sms_subscriber(user.subscription.sms_arn) is not False:
                    user.subscription.sms_arn = ''
                    
        if user.subscription.status == "APPROVED":
            if user.subscription.methods == "Both" or user.subscription.methods == "Email":
                if len(user.subscription.email) > 5:                
                    # Already subscribed?
                    try:
                        arn = current_email_subscribers[user.subscription.email]
                    except KeyError:
                        arn = put_email_subscriber(user.subscription.email)
                        if arn is False:
                            sns_error.send(app, func='update_user_subscriptions', e='Unable to put_email_subscriber')
                    # Change email address?
                    #if user.subscription.email_arn != '' or user.subscription.email_arn != 'PendingConfirmation':
                    if user.subscription.email_arn not in pending_or_emtpy:
                        if user.subscription.email_arn != arn:
                            debug("Going to delete %s" % user.subscription.email)
                            del_email_subscriber(user.subscription.email_arn)
                    user.subscription.email_arn = arn
                
            if user.subscription.methods == "Both" or user.subscription.methods == "SMS Phone":
                if len(user.subscription.smsPhone) > 7:
                    # Already subscribed?
                    try:
                        arn = current_sms_subscribers['1' + user.subscription.smsPhone]
                    except KeyError:
                        arn = put_sms_subscriber('1' + user.subscription.smsPhone)
                        if arn is False:
                            sns_error.send(app, func='update_user_subscriptions', e='Unable to put_sms_subscriber')
                    # Change sms number?
                    #if user.subscription.sms_arn != '' or user.subscription.sms_arn != 'PendingConfirmation':
                    if user.subscription.sms_arn not in pending_or_emtpy:
                        if user.subscription.sms_arn != arn:
                            debug("Going to delete %s" % user.subscription.smsPhone)
                            del_sms_subscriber(user.subscription.sms_arn)
                    user.subscription.sms_arn = arn
                    
        debug(user.subscription.email_arn)
        debug(user.subscription.sms_arn)           
        user.save()
        return True
        '''
        if user.subscription.email:
            current_subscribers = get_email_subscribers()
            try:
                user.subscription.email_arn = current_subscribers[user.subscription.email]
                if user.subscription.status != "APPROVED" or (user.subscription.methods != "Both" and user.subscription.methods != "Email"):
                    if del_email_subscriber(user.subscription.email_arn) not False:
                        user.subscription.email_arn = ''
            except KeyError:
                if user.subscription.status == "APPROVED":
                    if user.subscription.methods == "Both" or user.subscription.methods == "Email":
                        user.subscription.email_arn = put_email_subscriber(user.subscription.email)
                        if user.subscription.email_arn is False:
                            sns_error.send(app, func='update_user_subscriptions', e='Unable to put_email_subscriber')
                        
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
        '''

    
    
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
