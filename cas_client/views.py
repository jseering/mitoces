#!/usr/bin/python

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Module, Outcome, Keyword
from django.contrib.auth.models import User
from forms import ModuleForm, UserForm
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from operator import *

#-----------------------------------------------------------------------------
# index

@login_required
def index(request):
    context ={}
    latest_module_list = Module.objects.all().order_by('-date')[:10]
    user_module_list   = Module.objects.filter(creator=request.user).order_by('-date')[:5]
    return render_to_response('index.html', {'latest_module_list': latest_module_list, 'user_module_list': user_module_list},RequestContext(request,context))

def explore(request):
    context = {}
    return render_to_response('explore.html', RequestContext(request,context))

def create(request):
    context = {}
    if request.POST:
        form = ModuleForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/modules/')
    else:
        form = ModuleForm(user=request.user)
    args = {}
    args.update(csrf(request))
    args['form'] = form   
    return render_to_response('create.html', args, RequestContext(request,context))

def module(request, module_id):
    context = {}
    module = get_object_or_404(Module, id=module_id)
    return render_to_response('module_detail.html', {'module': module}, RequestContext(request,context))

def modules(request):
    context = {}
    module_list = Module.objects.all().order_by('-date')
    args = {}
    args.update(csrf(request))
    args['module_list'] = module_list
    return render_to_response('modules.html', args, RequestContext(request,context))

def search(request):
    context = {}
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    if search_text == '':
        modules = {}
        keywords = {}
        users = {}
    else:
        modules = Module.objects.filter(name__contains=search_text)
        outcomes = Outcome.objects.filter(name__contains=search_text)
        keywords = Keyword.objects.filter(name__contains=search_text)
        users = User.objects.filter(username__contains=search_text)
    return render_to_response('ajax_search.html', {'modules': modules, 'outcomes': outcomes, 'keywords': keywords, 'users': users}, RequestContext(request,context))

def create_name_keyword(request):
    context = {}
    if request.method == "POST":
        name_text = request.POST['name_text']
        name_text = name_text.strip()
    else:
        name_text = ''
    if name_text == '':
        keywords = {}
    else:
        words_in_name_text = name_text.split(' ');
        keywords = Keyword.objects.filter(reduce(or_, (Q(name__contains=word.strip()) for word in words_in_name_text)))
    return render_to_response('ajax_keyword_recommendations.html', {'keywords': keywords}, RequestContext(request,context))

def create_name_outcome(request):
    context = {}
    if request.method == "POST":
        name_text = request.POST['name_text']
        name_text = name_text.strip()
    else:
        name_text = ''
    if name_text == '':
        outcomes = {}
    else:
        words_in_name_text = name_text.split(' ');
        outcomes = Outcome.objects.filter(reduce(or_, (Q(name__contains=word.strip()) for word in words_in_name_text)))
    return render_to_response('ajax_outcome_recommendations.html', {'outcomes': outcomes}, RequestContext(request,context))

def outcome(request, outcome_id):
    context = {}
    outcome_ = get_object_or_404(Outcome, id=outcome_id)
    module_list = Module.objects.filter(outcomes__name__contains=outcome_).order_by('-date')
    return render_to_response('outcome_detail.html', {'outcome': outcome_, 'module_list': module_list}, RequestContext(request,context))
    
def outcomes(request):
    context = {}
    outcome_list = Outcome.objects.all()
    return render_to_response('outcomes.html', {'outcome_list': outcome_list}, RequestContext(request,context))

def keyword(request, keyword_id):
    context = {}
    keyword_ = get_object_or_404(Keyword, id=keyword_id)
    module_list = Module.objects.filter(keywords__name__contains=keyword_).order_by('-date')
    return render_to_response('keyword_detail.html', {'keyword': keyword_, 'module_list': module_list}, RequestContext(request,context))

def keywords(request):
	context = {}
	keyword_list = Keyword.objects.all()
	args = {}
	args['keyword_list'] = keyword_list
	return render_to_response('keywords.html', args, RequestContext(request,context))

def edit_profile(request):
    context = {}
    if request.POST:
        try:
            u = User.objects.get(username=request.user)
            form = UserForm(request.POST, instance=u)
        except ObjectDoesNotExist:
            form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/users/')
    else:
        try:
            u = User.objects.get(username=request.user)
            form = UserForm(instance=u)
        except ObjectDoesNotExist:
            form = UserForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('edit_profile.html', args, RequestContext(request,context))

def user(request, user_id):
    context = {}
    this_user    = get_object_or_404(User, id=user_id)
    user_module_list = Module.objects.filter(creator=this_user).order_by('-date')
    return render_to_response('user_detail.html', {'this_user': this_user, 'user_module_list': user_module_list}, RequestContext(request,context))

def users(request):
    context = {}
    user_list = User.objects.all()
    return render_to_response('users.html', {'user_list': user_list}, RequestContext(request,context))
