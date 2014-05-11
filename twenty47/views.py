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

from flask import Blueprint, request, redirect, render_template, url_for, flash
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form
from twenty47.models import Dispatch, IncidentType, UnitsImpacted, AssistanceRequested
from twenty47.forms import DispatchForm
from twenty47 import db, app, debug, dispatch_created
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
            if role.name == 'Admin':
                next_url = url_for('dispatch.dispatch_create')
            if role.name == 'User':
                next_url = url_for('dispatch.dispatch_create')
        return next_url
        
class DispatchCreate(MethodView):
    decorators = [login_required, roles_accepted('User', 'Admin')]
    
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
    

# Register the urls
dispatch.add_url_rule('/', view_func=Home.as_view('index'))
dispatch.add_url_rule('/dispatch/create', defaults={'id': None},view_func=DispatchCreate.as_view('dispatch_create'))
