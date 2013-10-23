#!/usr/bin/python

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Department, Subject, Module, Outcome, Keyword
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from operator import *
from django.forms.models import modelformset_factory
from django.utils.html import escape, escapejs
from django.utils import simplejson
from random import choice

#-----------------------------------------------------------------------------
# index

@login_required
def index(request):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusmodule = choice(modules)
    focusmodule.outcomes = Outcome.objects.filter(modules__name=focusmodule)
    return render_to_response('index.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusmodule': focusmodule}, RequestContext(request,context))

@login_required
def profile(request,user_id):
    context = {}
    thisuser = User.objects.get(id=user_id)
    thisuser.subjects = Subject.objects.filter(instructors=thisuser)
    thisuser.modules = Module.objects.filter(instructors=thisuser)
    thisuser.outcomes = Outcome.objects.filter(instructors=thisuser)
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    return render_to_response('profile.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'thisuser': thisuser}, RequestContext(request,context))

@login_required
def module(request,module_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusmodule = Module.objects.get(id=module_id)
    focusmodule.outcomes = Outcome.objects.filter(modules__id=focusmodule.id)
    return render_to_response('module.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusmodule': focusmodule}, RequestContext(request,context))

@login_required
def outcome(request,outcome_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusoutcome = Outcome.objects.get(id=outcome_id)
    return render_to_response('outcome.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusoutcome': focusoutcome}, RequestContext(request,context))

@login_required
def subject(request,subject_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focussubject = Subject.objects.get(id=subject_id)
    focussubject.modules = Module.objects.filter(subjects__id=focussubject.id)
    return render_to_response('subject.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focussubject': focussubject}, RequestContext(request,context))

@login_required
def department(request,department_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusdepartment = Department.objects.get(id=department_id)
    focusdepartment.subjects = Subject.objects.filter(number__startswith=focusdepartment.name)
    return render_to_response('department.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusdepartment': focusdepartment}, RequestContext(request,context))

# === Editing ===
@login_required
def edit_outcome(request,outcome_id):
    focusoutcome = Outcome.objects.get(id=outcome_id)
    if not(request.user in focusoutcome.instructors.all()): # unauthorized access
        HttpResponseRedirect('/outcomes/{{ focusoutcome.id }}/')
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    return render_to_response('edit_outcome.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusoutcome': focusoutcome}, RequestContext(request,context))

@login_required
def edit_module(request,module_id):
    focusmodule = Module.objects.get(id=module_id)
    if not(request.user in focusmodule.instructors.all()): # unauthorized access
        HttpResponseRedirect('/modules/{{ focusmodule.id }}/')
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusmodule.outcomes = Outcome.objects.filter(modules__id=focusmodule.id)
    return render_to_response('edit_module.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusmodule': focusmodule}, RequestContext(request,context))

@login_required
def edit_subject(request,subject_id):
    focussubject = Subject.objects.get(id=subject_id)
    if not(request.user in focussubject.instructors.all()): # unauthorized access
        HttpResponseRedirect('/subjects/{{ focussubject.id }}/')
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focussubject.modules = Module.objects.filter(subjects__id=focussubject.id)
    return render_to_response('edit_subject.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focussubject': focussubject}, RequestContext(request,context))

# === Deleting (via AJAX) ===
@login_required
def delete_outcome(request,outcome_id):
    focusoutcome = Outcome.objects.get(id=outcome_id)
    if not(request.user in focusoutcome.instructors.all()): # unauthorized access
        to_json = {
            'result': 'failed'
        }
        return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    focusoutcome.delete()
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def delete_module(request,module_id):
    focusmodule = Module.objects.get(id=module_id)
    if not(request.user in focusmodule.instructors.all()): # unauthorized access
        to_json = {
            'result': 'failed'
        }
        return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    focusmodule.delete()
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def delete_subject(request,subject_id):
    focussubject = Subject.objects.get(id=subject_id)
    if not(request.user in focussubject.instructors.all()): # unauthorized access
        to_json = {
            'result': 'failed'
        }
        return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    focussubject.delete()
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def remove_outcome_from_module(request,module_id,outcome_id):
    outcome = Outcome.objects.get(id=outcome_id)
    module = Module.objects.get(id=module_id)   
    outcome.modules.remove(module)
    # TODO: Figure out how to check if this fails, and return 'result': 'failed'
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")



