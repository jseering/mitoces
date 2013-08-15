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
    context ={}
    latest_module_list = Module.objects.all().order_by('-date')[:10]
    user_module_list   = Module.objects.filter(creator=request.user).order_by('-date')[:5]
    return render_to_response('index.html', {'latest_module_list': latest_module_list, 'user_module_list': user_module_list},RequestContext(request,context))

def explore(request):
	context = {}
	module_all = Module.objects.all()
	module_outcomes = {}
	module_keywords = {}
	for module in module_all:
		module_outcomes[module.name]=[]
		module_keywords[module.name] = []
		for outcome in module.outcomes.all():
			module_outcomes[module.name].append(outcome.name)
		for keyword in module.keywords.all():
			module_keywords[module.name].append(keyword.name)
	return render_to_response('explore.html',{"module_all":module_all,"module_outcomes":module_outcomes,"module_keywords":module_keywords},RequestContext(request,context))	

def explore_keyword(request,keyword):
	name = Keyword.objects.get(name=keyword)
	modules = Module.objects.filter(keywords=name)
	module_names = [x.name for x in modules]
	module_outcomes = {}
	for module in modules:
		module_outcomes[module.name] = []
		for outcome in module.outcomes.all():
			module_outcomes[module.name].append(outcome.name)
	context = {'module_names':module_names,'module_outcomes':module_outcomes}
	return HttpResponse(simplejson.dumps(context),content_type="application/json")

def explore_outcome(request,outcome):
	name = Outcome.objects.get(name=outcome)
	modules = Module.objects.filter(outcomes=name)
	module_names = [x.name for x in modules]
	module_keywords = {}
	for module in modules:
		module_keywords[module.name] = []
		for keyword in module.keywords.all():
			module_keywords[module.name].append(keyword.name)
	context ={'module_names':module_names,'module_keywords':module_keywords}
	return HttpResponse(simplejson.dumps(context),content_type="application/json")

def module_id(request,module):
    name = Module.objects.get(name=module)
    id = name.id
    return HttpResponse(id)

def outcome_id(request,outcome):
    name = Outcome.objects.get(name=outcome)
    id = name.id
    return HttpResponse(id)

def keyword_id(request,keyword):
    name = Keyword.objects.get(name=keyword)
    id = name.id
    return HttpResponse(id)

def exploresearch(request):
    context = {}
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    if search_text == '':
        modules = {}
        outcomes = {}
        keywords = {}
        users = {}
    else:
        modules = Module.objects.filter(name__contains=search_text)
        outcomes = Outcome.objects.filter(name__contains=search_text)
        keywords = Keyword.objects.filter(name__contains=search_text)
        users = User.objects.filter(username__contains=search_text)
    return render_to_response('explore_search.html', {'modules': modules, 'outcomes': outcomes, 'keywords': keywords}, context_instance=RequestContext(request))

def add_outcome(request):
    context = {}
    if request.POST:
        form = OutcomeForm(request.POST)
        if form.is_valid():
            obj = form.save()
            pk_value = obj._get_pk_val()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(pk_value), escapejs(obj)))
    else:
        form = OutcomeForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('add_outcome.html', args, RequestContext(request,context))

def add_keyword(request):
    context = {}
    if request.POST:
        form = KeywordForm(request.POST)
        if form.is_valid():
            obj = form.save()
            pk_value = obj._get_pk_val()
            return HttpResponse('<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' % (escape(pk_value), escapejs(obj)))
    else:
        form = KeywordForm()
    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render_to_response('add_keyword.html', args, RequestContext(request,context))

def new_keyword(request):
    context = {}
    if request.POST:
        kw, created = Keyword.objects.get_or_create(name=request.POST['keyword_name'])
    else:
        kw = {}
    return render_to_response('ajax_new_keyword.html', {'keyword': kw}, RequestContext(request,context))

def new_outcome(request):
    context = {}
    if request.POST:
        oc, created = Outcome.objects.get_or_create(name=request.POST['outcome_name'],description=request.POST['outcome_description'])
    else:
        oc = {}
    return render_to_response('ajax_new_outcome.html', {'outcome': oc}, RequestContext(request,context))

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

def create_formset(request):
    context = {}
    ModuleFormSet = modelformset_factory(Module)
    if request.POST:
        formset = ModuleFormSet(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = ModuleFormSet()
    args = {}
    args.update(csrf(request))
    args['formset'] = formset   
    return render_to_response('create_formset.html', args, RequestContext(request,context))

def delete_module(request):
    context = {}
    if request.method == "POST":
        module_id = request.POST['module_id']
        module = Module.objects.get(pk=module_id).delete()
    return render_to_response('modules.html', RequestContext(request,context))

def edit_module(request, module_id):
    context = {}
    return render_to_response('edit_module.html', {'module': module}, RequestContext(request,context))

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

def outcome_search(request):
    context = {}
    if request.method == "POST":
        outcome_search_text = request.POST['outcome_search_text']
    else:
        outcome_search_text = ''
    if outcome_search_text == '':
        outcomes = {}
    else:
        # do some tricky searching/filtering
        # first break the text into individual words
        words = outcome_search_text.split(' ');
        print "\n words = ", words, "\n"
        # then remove inconsequential words from the list of words (e.g., and, the, or, but, etc.)
        useless_words = ["the","and","if","but","between","over","through","on","an"]
        important_words = list(set(words)-set(useless_words))
        # then find all outcomes that contain at least two of the same words in the description
        min_words_match = 2
        outcomes = Outcome.objects.filter(description__contains=important_words[0]) # TODO: JUST DOING FIRST IMPORTANT WORD RIGHT NOW!!
        print "\n outcome = ", outcomes, "\n"
    return render_to_response('ajax_outcome_search.html', {'outcomes': outcomes}, RequestContext(request,context))

def keyword_search(request):
    context = {}
    if request.method == "POST":
        keyword_search_text = request.POST['keyword_search_text']
    else:
        keyword_search_text = ''
    if keyword_search_text == '':
        keywords = {}
    else:
        keywords = Keyword.objects.filter(name__contains=keyword_search_text)
    return render_to_response('ajax_keyword_search.html', {'keywords': keywords}, RequestContext(request,context))

def search(request):
    context = {}
    if request.method == "POST":
        search_text = request.POST['search_text']
    else:
        search_text = ''
    if search_text == '':
        modules = {}
        keywords = {}
        outcomes = {}
        users = {}
    else:
        modules = Module.objects.filter(name__contains=search_text)
        outcomes = Outcome.objects.filter(name__contains=search_text)
        keywords = Keyword.objects.filter(name__contains=search_text)
        users = User.objects.filter(username__contains=search_text)
    return render_to_response('ajax_search.html', {'modules': modules, 'outcomes': outcomes, 'keywords': keywords, 'users': users}, RequestContext(request,context))

def create_outcome_keyword(request):
    context = {}
    if request.method == "POST":
        selected_outcome_ids = request.POST.getlist('selected_outcome_ids[]')
    else:
        selected_outcome_ids = {}
    print selected_outcome_ids
    if not selected_outcome_ids:
        keywords = {}
    else:
        # for each outcome in selected outcomes, find the modules that use that outcome, and get that modules keywords
        keywords = []
        for outcome_id in selected_outcome_ids:
            print "outcome_id =",outcome_id
            name = Outcome.objects.get(id=outcome_id)
            modules = Module.objects.filter(outcomes=name)
            for module in modules:
                keywords.extend(module.keywords.all())
        # get rid of duplicates using reduce
        print "\n\n"
        print "keywords =",keywords
        keywords = list(set(keywords))
        print "keywords after reduce =",keywords
    return render_to_response('ajax_keyword_recommendations.html', {'keywords': keywords}, RequestContext(request,context))

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
