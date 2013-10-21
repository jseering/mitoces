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
    print focussubject.modules
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




