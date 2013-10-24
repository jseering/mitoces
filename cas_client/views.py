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
    outcome_prereqs = {}
    for outcome in focusmodule.outcomes.all():
        outcome_prereqs[outcome.name] = []
        for prereq in outcome.prerequisites.all():
            outcome_prereqs[outcome.name].append(prereq.name)
    return render_to_response('module.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusmodule': focusmodule, 'outcome_prereqs': outcome_prereqs}, RequestContext(request,context))

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

@login_required
def remove_subject_from_outcome(request,outcome_id,subject_id):
    outcome = Outcome.objects.get(id=outcome_id)
    subject = Subject.objects.get(id=subject_id)   
    outcome.subjects.remove(subject)
    # TODO: Figure out how to check if this fails, and return 'result': 'failed'
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def remove_instructor_from_outcome(request,outcome_id,instructor_id):
    outcome = Outcome.objects.get(id=outcome_id)
    instructor = User.objects.get(id=instructor_id)   
    outcome.instructors.remove(instructor)
    # TODO: Figure out how to check if this fails, and return 'result': 'failed'
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def remove_prereq_from_outcome(request,outcome_id,prereq_id):
    outcome = Outcome.objects.get(id=outcome_id)
    prereq = Outcome.objects.get(id=prereq_id)   
    outcome.prerequisites.remove(prereq)
    # TODO: Figure out how to check if this fails, and return 'result': 'failed'
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

# Edit name
@login_required
def edit_outcome_name(request,outcome_id):
    outcome = Outcome.objects.get(id=outcome_id)
    if request.method=="POST":
        newname = request.POST.get('newname','')
        if newname=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            outcome.name = newname
            outcome.save()
            to_json = {
                'result': 'succeeded'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def edit_module_name(request,module_id):
    module = Module.objects.get(id=module_id)
    if request.method=="POST":
        newname = request.POST.get('newname','')
        if newname=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            module.name = newname
            module.save()
            to_json = {
                'result': 'succeeded'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

# Edit description
@login_required
def edit_outcome_description(request,outcome_id):
    outcome = Outcome.objects.get(id=outcome_id)
    if request.method=="POST":
        newdescription = request.POST.get('newdescription','')
        if newdescription=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            outcome.description = newdescription
            outcome.save()
            to_json = {
                'result': 'succeeded'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

# Add 
@login_required
def add_module(request):
    context = {}
    context['user'] = request.user
    if request.method=="POST":
        module_name = request.POST.get('module_name','')
        module_description = request.POST.get('module_description','')
        module_creator_id = request.POST.get('module_creator_id','')
        if module_name=='' or module_description=='' or module_creator_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            module_creator = User.objects.get(id=module_creator_id)
            module = Module(name=module_name,description=module_description,creator=module_creator)
            module.save()
            module.instructors.add(module_creator)
            to_json = {
                'result': 'succeeded',
                'new_module_id': module.id
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    return render_to_response('add_module.html', context, RequestContext(request,context))




