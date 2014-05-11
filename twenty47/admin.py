#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  admin.py
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
Module admin.py documentation
Sets up the admin for Twenty47
"""
from flask import Blueprint, request, redirect, render_template, url_for, flash, abort
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from flask.ext.security import login_required, roles_required, script
from twenty47.models import Role, User, user_datastore, Subscriber, \
        IncidentType, UnitsImpacted, AssistanceRequested
from twenty47 import app, debug, subscription_updated, sns_error
from twenty47 import utils
from itsdangerous import BadSignature

admin = Blueprint('admin', __name__, template_folder='templates')

class Pager(MethodView):
    decorators = [login_required, roles_required('Admin')]
    cls = User
    
    def get(self, page=1):
        #Buj
        #debug(utils.get_activation_link('5367f1e79b986c933f88e6d9', 'makeregistered'), 'notice')
        #debug(utils.get_users_with_role(role_name='SubMan', list_of='email'))
        
        users = self.cls.objects.paginate(page=page, per_page=20)
        return render_template('admin/pager.html', users=users)
   
class List(MethodView):
    decorators = [login_required, roles_required('Admin')]
    clsRole = Role
    clsIncidentTypes = IncidentType
    clsUnitsImpacted = UnitsImpacted
    clsAssistanceRequested = AssistanceRequested

    def get(self):
        roles = self.clsRole.objects.all()
        incidenttypes = self.clsIncidentTypes.objects.all().order_by('order')
        unitsimpacted = self.clsUnitsImpacted.objects.all().order_by('order')
        assistancerequested = self.clsAssistanceRequested.objects.all().order_by('order')
        context = {
            "roles": roles,
            "incidenttypes": incidenttypes,
            "unitsimpacted": unitsimpacted,
            "assistancerequested": assistancerequested,
        }
        
        
        return render_template('admin/list.html', **context)

class Detail(MethodView):
    decorators = [login_required, roles_required('Admin')]

    def get_context(self, uid=None, action=None):
        form_cls = model_form(User, field_args = {
            'firstName': {'label': 'First Name'},
            'lastName': {'label': 'Last Name'},
            })
        del form_cls.created_at
        del form_cls.modified_at
        del form_cls.active
        del form_cls.confirmed_at
        del form_cls.last_login_at
        del form_cls.current_login_at
        del form_cls.last_login_ip
        del form_cls.current_login_ip
        del form_cls.login_count
        #del form_cls.roles
        #del form_cls.password
        del form_cls.subscription
        

        if uid:
            del form_cls.password
            user = User.objects.get_or_404(id=uid)
            if request.method == 'POST':
                form = form_cls(request.form, inital=user._data)
            else:
                form = form_cls(obj=user)
        else:
            user = User()
            form = form_cls(request.form)

        form.roles.label_attr='name'
        context = {
            "user": user,
            "form": form,
            "create": uid is None
        }
        return context
        
                
    def get(self, uid):
        context = self.get_context(uid)
        return render_template('admin/detail.html', **context)

    def post(self, uid):        
        context = self.get_context(uid)
        form = context.get('form')
        
        try:
            if request.form['action'] == "none":
                if set_subscription_status(context.get('user'), "NONE"):
                    return "True"
                else:
                    return(app.config['DISPATCH_ERROR_GENERAL'])
            elif request.form['action'] == "denied":
                if set_subscription_status(context.get('user'), "DENIED"):
                    return "True"
                else:
                    return(app.config['DISPATCH_ERROR_GENERAL'])
            elif request.form['action'] == "pending":
                if set_subscription_status(context.get('user'), "PENDING"):
                    return "True"
                else:
                    return(app.config['DISPATCH_ERROR_GENERAL'])
            elif request.form['action'] == "approved":
                if set_subscription_status(context.get('user'), "APPROVED"):
                    return "True"
                else:
                    return(app.config['DISPATCH_ERROR_GENERAL'])
            elif request.form['action'] == "activate":
                user_datastore.activate_user(user=context.get('user'))
                return "True"
            elif request.form['action'] == "deactivate":
                user_datastore.deactivate_user(user=context.get('user'))
                return "True"
            else:
                flash("Action failed, " + request.form['action'], 'danger')
            
            return redirect(url_for('admin.user_list'))
        except KeyError, e:
            pass

        if form.validate():
            user = context.get('user')
            form.populate_obj(user)
            if uid:
                user.save()
            else:
                user_datastore.create_user(firstName=user.firstName, 
                    lastName=user.lastName, password=user.password, 
                    email=user.email, comments=user.comments)

            return redirect(url_for('admin.user_list'))
        return render_template('admin/detail.html', **context)
        

        
class Remove(MethodView):
    decorators = [login_required, roles_required('Admin')]
    
    def get_context(self, id=None, action=None):
        
        if id:
            if action == "user":
                target = User.objects.get_or_404(id=id)
                form = model_form(User, field_args = {
                    'firstName': {'label': 'First Name'},
                    'lastName': {'label': 'Last Name'},
                    })
                if request.method == 'POST':
                    form = form(request.form, inital=target._data)
                else:
                    form = form(obj=target)
            elif action == "role":
                target = Role.objects.get_or_404(id=id)
                form = model_form(Role)
                if request.method == 'POST':
                    form = form(request.form, inital=target._data)
                else:
                    form = form(obj=target)
                    
            form.roles.label_attr='name'
            context = {
                "action": action,
                "target": target,
                "form": form,
            }
            return context
                
        else:
            flash("Action failed, " + request.form['action'])
            return redirect(url_for('admin.index'))
            
    def get(self, id, action):
        context = self.get_context(id, action)
        return render_template('admin/remove.html', **context)
        
    def post(self, id, action):        
        context = self.get_context(id, action)
        form = context.get('form')
        
        if form.validate():
            target = context.get('target')
            if action == "user":
                user_datastore.delete_user(target)
            elif action == "role":
                pass


        return redirect(url_for('admin.index'))
    
        
class RoleDetail(MethodView):

    decorators = [login_required, roles_required('Admin')]

    def get_context(self, id=None):
        form_cls = model_form(Role)
        del form_cls.created_at
        del form_cls.modified_at

        if id:
            role = Role.objects.get_or_404(id=id)
            if request.method == 'POST':
                form = form_cls(request.form, inital=role._data)
            else:
                form = form_cls(obj=role)
        else:
            role = Role()
            form = form_cls(request.form)

        context = {
            "role": role,
            "form": form,
            "create": id is None
        }
        return context
        
    def get(self, id):
        context = self.get_context(id)
        return render_template('admin/roledetail.html', **context)

    def post(self, id):
        context = self.get_context(id)
        form = context.get('form')

        if form.validate():
            role = context.get('role')
            form.populate_obj(role)
            if id:
                role.save()
            else:
                user_datastore.create_role(name=role.name, 
                    description=role.description)
            flash("Role saved", 'success')
            return redirect(url_for('admin.index'))
        return render_template('admin/roledetail.html', **context)
        

class RemoteUserAdmin(MethodView):
    
    def get(self, payload):
        s = utils.get_serializer()
        try:
            paystr = s.loads(payload)
            listload =paystr.split(',')
            user_id = listload[0]
            action = listload[1]
        except BadSignature, e:
            abort(500)
            return
        
        print user_id
        print action
        user = User.objects.get_or_404(id=user_id)
        if action == "deactivate":
            # OK
            user_datastore.deactivate_user(user)
            completed_action = "Deactivated."
        elif action == "makeuser":
            # OK
            user_datastore.add_role_to_user(user, "User")
            completed_action = "has User role."
        elif action == "makeregistered":
            # OK
            user_datastore.add_role_to_user(user, "Registered")
            completed_action = "has Registered role."
        elif action == "subscriptiondeny":
            # OK
            set_subscription_status(user, "DENIED")
            completed_action = "subscriptions are denied."
        elif action == "subscriptionapprove":
            # OK
            set_subscription_status(user, "APPROVED")
            completed_action = "subscriptions are approved."
        else:
            flash(app.config['DISPATCH_ERROR_REMOTEADMIN'], 'danger')
            return redirect(url_for('dispatch.index'))        
        flash(user.firstName + " " + user.lastName + " " + completed_action, 'success')
        return redirect(url_for('dispatch.index'))


class DetailFactory(MethodView):

    decorators = [login_required, roles_required('Admin')]

    def get_context(self, id=None, action=None):
        if action == "IncidentType":
            form_cls = model_form(IncidentType)
            if id:
                target = IncidentType.objects.get_or_404(id=id)
                if request.method == 'POST':
                    form = form_cls(request.form, inital=target._data)
                else:
                    form = form_cls(obj=target)
            else:
                target = IncidentType()
                form = form_cls(request.form)
        elif action == "UnitsImpacted":
            form_cls = model_form(UnitsImpacted)
            if id:
                target = UnitsImpacted.objects.get_or_404(id=id)
                if request.method == 'POST':
                    form = form_cls(request.form, inital=target._data)
                else:
                    form = form_cls(obj=target)
            else:
                target = UnitsImpacted()
                form = form_cls(request.form)
        elif action == "AssistanceRequested":
            form_cls = model_form(AssistanceRequested)
            if id:
                target = AssistanceRequested.objects.get_or_404(id=id)
                if request.method == 'POST':
                    form = form_cls(request.form, inital=target._data)
                else:
                    form = form_cls(obj=target)
            else:
                target = AssistanceRequested()
                form = form_cls(request.form)

        context = {
            "action": action,
            "target": target,
            "form": form,
            "create": id is None
        }
        return context
        
                
    def get(self, action, id):
        context = self.get_context(id, action)
        return render_template('admin/detail_factory.html', **context)

    def post(self, id, action):        
        context = self.get_context(id, action)
        form = context.get('form')
        
        if form.validate():
            target = context.get('target')
            form.populate_obj(target)
            target.save()
            flash(target.name + " saved", 'success')
            return redirect(url_for('admin.index'))
        return render_template('admin/detail_factory.html', **context)


class RemoveFactory(MethodView):
    decorators = [login_required, roles_required('Admin')]
    
    def get_context(self, id=None, action=None):
        if id:
            if action == "IncidentType":
                form_cls = model_form(IncidentType)
                target = IncidentType.objects.get_or_404(id=id)
                    
            elif action == "UnitsImpacted":
                form_cls = model_form(UnitsImpacted)
                target = UnitsImpacted.objects.get_or_404(id=id)
            
            elif action == "AssistanceRequested":
                form_cls = model_form(AssistanceRequested)
                target = AssistanceRequested.objects.get_or_404(id=id)

            else:
                flash("Action failed, " + request.form['action'])
                return redirect(url_for('admin.index'))
                
            if request.method == 'POST':
                form = form_cls(request.form, inital=target._data)
            else:
                form = form_cls(obj=target)

            context = {
                "action": action,
                "target": target,
                "form": form,
                "create": id is None
            }
            return context
        
        else:
            flash("Action failed, " + request.form['action'], 'danger')
            return redirect(url_for('admin.index'))

    def get(self, id, action):
        context = self.get_context(id, action)
        return render_template('admin/remove_factory.html', **context)
        
    def post(self, id, action):        
        context = self.get_context(id, action)
        form = context.get('form')
        
        if form.validate():
            target = context.get('target')
            target.delete()
            flash("Target deleted", 'success')


        return redirect(url_for('admin.index'))

def enable_subscription(user):
    '''
    Deprecated
    '''
    user.subscription.enabled = True
    if user.save():
        utils.update_user_subscriptions(user)
        return True
    return False
    
def disable_subscription(user):
    '''
    Deprecated
    '''
    user.subscription.enabled = False
    if user.save():
        return True
    return False
    
def set_subscription_status(user, status):
    if not user.subscription:
        target = Subscriber()
        user.subscription = target
    user.subscription.status = status
    if user.save():
        subscription_updated.send(app, user=user)
        return True
    return False



# Register the urls
admin.add_url_rule('/admin/', view_func=List.as_view('index'))
admin.add_url_rule('/admin/users/', defaults={'page': 1}, view_func=Pager.as_view('user_list'))
admin.add_url_rule('/admin/users/page/<int:page>', view_func=Pager.as_view('user_pager'))
admin.add_url_rule('/admin/userCreate/', defaults={'uid': None}, view_func=Detail.as_view('user_create'))
admin.add_url_rule('/admin/userEdit/<uid>/', view_func=Detail.as_view('user_edit'))
admin.add_url_rule('/admin/roleCreate/', defaults={'id': None}, view_func=RoleDetail.as_view('role_create'))
admin.add_url_rule('/admin/roleEdit/<id>/', view_func=RoleDetail.as_view('role_edit'))
admin.add_url_rule('/admin/remove/<id>/<action>', view_func=Remove.as_view('remove'))
admin.add_url_rule('/admin/remoteAdmin/<payload>', view_func=RemoteUserAdmin.as_view('remote_admin'))
admin.add_url_rule('/admin/create/<action>', defaults={'id': None}, view_func=DetailFactory.as_view('create'))
admin.add_url_rule('/admin/update/<action>/<id>', view_func=DetailFactory.as_view('update'))
admin.add_url_rule('/admin/delete/<action>/<id>', view_func=RemoveFactory.as_view('delete'))
