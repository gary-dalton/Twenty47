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
Module admin_dispatch.py documentation
Sets up the admin for dispatch for Twenty47
"""
from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from flask.ext.security import login_required, roles_required, script
from twenty47.models import user_datastore, IncidentType, UnitsImpacted, \
        AssistanceRequested, Subscriber

admin_dispatch = Blueprint('admin_dispatch', __name__, template_folder='templates')


class List(MethodView):
    decorators = [login_required, roles_required('Admin')]
    clsIncidentTypes = IncidentType
    clsUnitsImpacted = UnitsImpacted
    clsAssistanceRequested = AssistanceRequested

    def get(self):
        incidenttypes = self.clsIncidentTypes.objects.all()
        unitsimpacted = self.clsUnitsImpacted.objects.all()
        assistancerequested = self.clsAssistanceRequested.objects.all()
        return render_template('admin_dispatch/list.html', 
                incidenttypes=incidenttypes, 
                unitsimpacted=unitsimpacted,
                assistancerequested=assistancerequested,
                )

class Detail(MethodView):

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
        return render_template('admin_dispatch/detail.html', **context)

    def post(self, id, action):        
        context = self.get_context(id, action)
        form = context.get('form')
        
        if form.validate():
            target = context.get('target')
            form.populate_obj(target)
            target.save()
            return redirect(url_for('admin_dispatch.index'))
        return render_template('admin_dispatch/detail.html', **context)
        
class Remove(MethodView):
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
            flash("Action failed, " + request.form['action'])
            return redirect(url_for('admin.index'))

    def get(self, id, action):
        context = self.get_context(id, action)
        return render_template('admin_dispatch/remove.html', **context)
        
    def post(self, id, action):        
        context = self.get_context(id, action)
        form = context.get('form')
        
        if form.validate():
            target = context.get('target')
            target.delete()
            flash("Target deleted")


        return redirect(url_for('admin_dispatch.index'))
        
class SubscriberList(MethodView):
    decorators = [login_required, roles_required('Admin')]
    clsSubscriber = Subscriber

    def get(self):
        subscribers = self.clsSubscriber.objects.all()
        return render_template('admin_dispatch/subscriber_list.html', 
                subscribers=subscribers, 
                )
    

# Register the urls
admin_dispatch.add_url_rule('/admin_dispatch/', view_func=List.as_view('index'))
admin_dispatch.add_url_rule('/admin_dispatch/create/<action>', defaults={'id': None}, view_func=Detail.as_view('create'))
admin_dispatch.add_url_rule('/admin_dispatch/update/<action>/<id>', view_func=Detail.as_view('update'))
admin_dispatch.add_url_rule('/admin_dispatch/delete/<action>/<id>', view_func=Remove.as_view('delete'))
admin_dispatch.add_url_rule('/admin_dispatch/updateSubscriber/<action>/<id>', view_func=Remove.as_view('update_subscriber'))
