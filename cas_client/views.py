#!/usr/bin/python

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Module, Outcome, Keyword
from django.contrib.auth.models import User
from forms import ModuleForm, UserForm, OutcomeForm, KeywordForm
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from operator import *
from django.forms.models import modelformset_factory
from django.utils.html import escape, escapejs
from django.utils import simplejson

#-----------------------------------------------------------------------------
# index

@login_required
def index(request):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    return render_to_response('index.html', {'departments': departments, 'subjects': subjects, 'modules': modules},RequestContext(request,context))
