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
    outcome_prereqs = {}
    outcome_all = list()
    for outcome in focusmodule.outcomes.all():
        outcome_all.append(outcome.name)
        outcome_prereqs[outcome.name] = []
        for prereq in outcome.prerequisites.all():
            outcome_prereqs[outcome.name].append(prereq.name)
    return render_to_response('index.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusmodule': focusmodule, 'outcome_prereqs': outcome_prereqs, 'outcome_all': outcome_all}, RequestContext(request,context))

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
    outcome_all = list()
    outcome_ids = list()
    outcome_colors = list()
    # prereqs from other modules: light green #00FF00
    # outcomes from this module: green #41A565
    # hover color: #0066CC
    for outcome in focusmodule.outcomes.all():
        outcome_colors.append('#41A565')
        outcome_all.append(outcome.name)
        outcome_ids.append(outcome.id)
        outcome_prereqs[outcome.name] = []
        for prereq in outcome.prerequisites.all():
            outcome_prereqs[outcome.name].append(prereq.name)
            # see if this prereq is contained in this module ... if not, add it to outcomes_all and make color light green
            modules_with_this_outcome = Module.objects.filter(outcome__id=prereq.id)
            if focusmodule not in modules_with_this_outcome:
                outcome_colors.append('#CC9999')
                outcome_all.append(prereq.name)
                outcome_ids.append(prereq.id)
                outcome_prereqs[prereq.name] = []
    return render_to_response('module.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusmodule': focusmodule, 'outcome_prereqs': outcome_prereqs, 'outcome_all': outcome_all, 'outcome_ids': outcome_ids, 'outcome_colors': outcome_colors}, RequestContext(request,context))

@login_required
def outcome(request,outcome_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusoutcome = Outcome.objects.get(id=outcome_id)
    outcome_prereqs = {}
    outcome_all = list()
    outcome_ids = list()
    outcome_all.append(focusoutcome.name)
    outcome_ids.append(focusoutcome.id)
    outcome_prereqs[focusoutcome.name] = []
    for prereq in focusoutcome.prerequisites.all():
        outcome_prereqs[focusoutcome.name].append(prereq.name)
        outcome_all.append(prereq.name)
        outcome_ids.append(prereq.id)
        outcome_prereqs[prereq.name] = []
    for postreq in Outcome.objects.filter(prerequisites__id=focusoutcome.id):
        outcome_all.append(postreq.name)
        outcome_ids.append(postreq.id)
        outcome_prereqs[postreq.name] = []
        outcome_prereqs[postreq.name].append(focusoutcome.name)
    return render_to_response('outcome.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusoutcome': focusoutcome, 'outcome_prereqs': outcome_prereqs, 'outcome_all': outcome_all, 'outcome_ids': outcome_ids}, RequestContext(request,context))

@login_required
def subject(request,subject_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focussubject = Subject.objects.get(id=subject_id)
    focussubject.modules = Module.objects.filter(subjects__id=focussubject.id)
    module_prereqs = {}
    module_all = list()
    module_ids = list()
    for module in focussubject.modules.all():
        module_all.append(module.name)
        module_ids.append(module.id)
        module_prereqs[module.name] = []
        for outcome in Outcome.objects.filter(modules__id=module.id):
            for prereq in outcome.prerequisites.all():
                for prereqmod in prereq.modules.all():
                    module_prereqs[module.name].append(prereqmod.name)
    return render_to_response('subject.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focussubject': focussubject,'module_prereqs': module_prereqs, 'module_all': module_all, 'module_ids': module_ids}, RequestContext(request,context))

@login_required
def department(request,department_id):
    context = {}
    departments = Department.objects.all()
    subjects = Subject.objects.all()
    modules = Module.objects.all()
    focusdepartment = Department.objects.get(id=department_id)
    focusdepartment.subjects = Subject.objects.filter(number__startswith=focusdepartment.name+".")
    subject_prereqs = {}
    subject_all = list()
    subject_ids = list()
    for subject in focusdepartment.subjects.all():
        subject_all.append(subject.fullname)
        subject_ids.append(subject.id)
        subject_prereqs[subject.fullname] = []
        for prereq in subject.prerequisites.all():
            subject_prereqs[subject.fullname].append(prereq.fullname)
    return render_to_response('department.html', {'departments': departments, 'subjects': subjects, 'modules': modules, 'focusdepartment': focusdepartment,'subject_prereqs': subject_prereqs, 'subject_all': subject_all, 'subject_ids': subject_ids}, RequestContext(request,context))

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
def remove_instructor_from_module(request,module_id,instructor_id):
    instructor = User.objects.get(id=instructor_id)
    module = Module.objects.get(id=module_id)   
    module.instructors.remove(instructor)
    # TODO: Figure out how to check if this fails, and return 'result': 'failed'
    to_json = {
        'result': 'succeeded'
    }
    return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def remove_instructor_from_subject(request,subject_id,instructor_id):
    instructor = User.objects.get(id=instructor_id)
    subject = Subject.objects.get(id=subject_id)   
    subject.instructors.remove(instructor)
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
def remove_subject_from_module(request,module_id,subject_id):
    module = Module.objects.get(id=module_id)
    subject = Subject.objects.get(id=subject_id)   
    module.subjects.remove(subject)
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

@login_required
def remove_prereq_from_subject(request,subject_id,prereq_id):
    subject = Subject.objects.get(id=subject_id)
    prereq = Subject.objects.get(id=prereq_id)   
    subject.prerequisites.remove(prereq)
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

@login_required
def edit_subject_name(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method=="POST":
        newname = request.POST.get('newname','')
        if newname=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            subject.name = newname
            subject.save()
            to_json = {
                'result': 'succeeded'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def edit_subject_number(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method=="POST":
        newnumber = request.POST.get('newnumber','')
        if newnumber=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            subject.number = newnumber
            subject.save()
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

@login_required
def edit_module_description(request,module_id):
    module = Module.objects.get(id=module_id)
    if request.method=="POST":
        newdescription = request.POST.get('newdescription','')
        if newdescription=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            module.description = newdescription
            module.save()
            to_json = {
                'result': 'succeeded'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

@login_required
def edit_subject_description(request,subject_id):
    subject = Subject.objects.get(id=subject_id)
    if request.method=="POST":
        newdescription = request.POST.get('newdescription','')
        if newdescription=='': # we don't allow empty names
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            subject.description = newdescription
            subject.save()
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

@login_required
def add_subject(request):
    context = {}
    context['user'] = request.user
    if request.method=="POST":
        subject_number = request.POST.get('subject_number','')
        subject_name = request.POST.get('subject_name','')
        subject_description = request.POST.get('subject_description','')
        subject_creator_id = request.POST.get('subject_creator_id','')
        if subject_number=='' or subject_name=='' or subject_description=='' or subject_creator_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            subject_creator = User.objects.get(id=subject_creator_id)
            subject = Subject(number=subject_number,name=subject_name,description=subject_description,creator=subject_creator)
            subject.save()
            subject.instructors.add(subject_creator)
            to_json = {
                'result': 'succeeded',
                'new_subject_id': subject.id
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    return render_to_response('add_subject.html', context, RequestContext(request,context))

def add_outcome_to_module(request,module_id):
    context = {}
    context['user'] = request.user
    this_module = Module.objects.get(id=module_id)
    context['module'] = this_module
    if request.method=="POST":
        module_id = request.POST.get('module_id','')
        outcome_name = request.POST.get('outcome_name','')
        outcome_description = request.POST.get('outcome_description','')
        outcome_creator_id = request.POST.get('outcome_creator_id','')
        if outcome_name=='' or outcome_description=='' or outcome_creator_id=='' or module_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            outcome_creator = User.objects.get(id=outcome_creator_id)
            outcome = Outcome(name=outcome_name,description=outcome_description,creator=outcome_creator)
            outcome.save()
            outcome.instructors.add(outcome_creator)
            outcome.modules.add(this_module)
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['outcomes'] = Outcome.objects.all()
    return render_to_response('add_outcome_to_module.html', context, RequestContext(request,context))

def add_existing_outcome_to_module(request,module_id,outcome_id):
    if request.method=="POST":
        module_id = request.POST.get('module_id','')
        outcome_id = request.POST.get('outcome_id','')
        if outcome_id=='' or module_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            this_module = Module.objects.get(id=module_id)
            outcome = Outcome.objects.get(id=outcome_id)
            outcome.modules.add(this_module)
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def add_instructor_to_module(request,module_id):
    context = {}
    context['user'] = request.user
    this_module = Module.objects.get(id=module_id)
    context['module'] = this_module
    if request.method=="POST":
        module_id = request.POST.get('module_id','')
        incl_on_outcomes = request.POST.get('incl_on_outcomes','')
        instructor_id = request.POST.get('instructor_id','')
        if instructor_id=='' or module_id=='' or incl_on_outcomes=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            instructor = User.objects.get(id=instructor_id)
            this_module.instructors.add(instructor)
            this_module.save()
            if (int(incl_on_outcomes)==1):
                for outcome in Outcome.objects.filter(modules__id=module_id):
                    outcome.instructors.add(instructor)
                    outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['users'] = User.objects.all()
        context['module_instructors'] = this_module.instructors.all()
        return render_to_response('add_instructor_to_module.html', context, RequestContext(request,context))

def add_prereq_to_outcome(request,outcome_id):
    context = {}
    context['user'] = request.user
    this_outcome = Outcome.objects.get(id=outcome_id)
    context['outcome'] = this_outcome
    if request.method=="POST":
        outcome_id = request.POST.get('outcome_id','')
        prereq_name = request.POST.get('prereq_name','')
        prereq_description = request.POST.get('prereq_description','')
        prereq_creator_id = request.POST.get('prereq_creator_id','')
        if prereq_name=='' or prereq_description=='' or prereq_creator_id=='' or outcome_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            prereq_creator = User.objects.get(id=prereq_creator_id)
            prereq = Outcome(name=prereq_name,description=prereq_description,creator=prereq_creator)
            prereq.save()
            prereq.instructors.add(prereq_creator)
            this_outcome.prerequisites.add(prereq)
            this_outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['outcomes'] = Outcome.objects.all()
        context['outcome_prereqs'] = this_outcome.prerequisites.all()
        return render_to_response('add_prereq_to_outcome.html', context, RequestContext(request,context))

def add_existing_prereq_to_outcome(request,outcome_id,prereq_id):
    if request.method=="POST":
        outcome_id = request.POST.get('outcome_id','')
        prereq_id = request.POST.get('prereq_id','')
        if outcome_id=='' or prereq_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            this_outcome = Outcome.objects.get(id=outcome_id)
            prereq = Outcome.objects.get(id=prereq_id)
            this_outcome.prerequisites.add(prereq)
            this_outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def add_instructor_to_outcome(request,outcome_id):
    context = {}
    context['user'] = request.user
    this_outcome = Outcome.objects.get(id=outcome_id)
    context['outcome'] = this_outcome
    if request.method=="POST":
        outcome_id = request.POST.get('outcome_id','')
        instructor_id = request.POST.get('instructor_id','')
        if instructor_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            instructor = User.objects.get(id=instructor_id)
            this_outcome.instructors.add(instructor)
            this_outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['users'] = User.objects.all()
        context['outcome_instructors'] = this_outcome.instructors.all()
        return render_to_response('add_instructor_to_outcome.html', context, RequestContext(request,context))

def add_subject_to_outcome(request,outcome_id):
    context = {}
    context['user'] = request.user
    this_outcome = Outcome.objects.get(id=outcome_id)
    context['outcome'] = this_outcome
    if request.method=="POST":
        outcome_id = request.POST.get('outcome_id','')
        subject_id = request.POST.get('subject_id','')
        if subject_id=='' or outcome_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            subject = Subject.objects.get(id=subject_id)
            this_outcome.subjects.add(subject)
            this_outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['subjects'] = Subject.objects.all()
        context['outcome_subjects'] = this_outcome.subjects.all()
        return render_to_response('add_subject_to_outcome.html', context, RequestContext(request,context))

def add_subject_to_module(request,module_id):
    context = {}
    context['user'] = request.user
    this_module = Module.objects.get(id=module_id)
    context['module'] = this_module
    if request.method=="POST":
        print "posting..."
        module_id = request.POST.get('module_id','')
        subject_id = request.POST.get('subject_id','')
        if subject_id=='' or module_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            subject = Subject.objects.get(id=subject_id)
            this_module.subjects.add(subject)
            this_module.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['subjects'] = Subject.objects.all()
        context['module_subjects'] = this_module.subjects.all()
        return render_to_response('add_subject_to_module.html', context, RequestContext(request,context))

def add_module_to_outcome(request,outcome_id):
    context = {}
    context['user'] = request.user
    this_outcome = Outcome.objects.get(id=outcome_id)
    context['outcome'] = this_outcome
    if request.method=="POST":
        outcome_id = request.POST.get('outcome_id','')
        module_name = request.POST.get('module_name','')
        module_description = request.POST.get('module_description','')
        module_creator_id = request.POST.get('module_creator_id','')
        if module_name=='' or module_description=='' or module_creator_id=='' or outcome_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            module_creator = User.objects.get(id=module_creator_id)
            module = Module(name=module_name,description=module_description,creator=module_creator)
            module.save()
            module.instructors.add(module_creator)
            this_outcome.modules.add(module)
            this_outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['modules'] = Module.objects.all()
        context['outcome_modules'] = this_outcome.modules.all()
        return render_to_response('add_module_to_outcome.html', context, RequestContext(request,context))

def add_existing_module_to_outcome(request,outcome_id,module_id):
    if request.method=="POST":
        outcome_id = request.POST.get('outcome_id','')
        module_id = request.POST.get('module_id','')
        if outcome_id=='' or module_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            this_outcome = Outcome.objects.get(id=outcome_id)
            module = Module.objects.get(id=module_id)
            this_outcome.modules.add(module)
            this_outcome.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def add_module_to_subject(request,subject_id):
    context = {}
    context['user'] = request.user
    this_subject = Subject.objects.get(id=subject_id)
    context['subject'] = this_subject
    if request.method=="POST":
        subject_id = request.POST.get('subject_id','')
        module_name = request.POST.get('module_name','')
        module_description = request.POST.get('module_description','')
        module_creator_id = request.POST.get('module_creator_id','')
        if module_name=='' or module_description=='' or module_creator_id=='' or subject_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            module_creator = User.objects.get(id=module_creator_id)
            module = Module(name=module_name,description=module_description,creator=module_creator)
            module.save()
            module.instructors.add(module_creator)
            this_subject = Subject.objects.get(id=subject_id)
            module.subjects.add(this_subject)
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['modules'] = Module.objects.all()
        context['subject_modules'] = Module.objects.filter(subjects__id=subject_id)
        return render_to_response('add_module_to_subject.html', context, RequestContext(request,context))

def add_existing_module_to_subject(request,subject_id,module_id):
    if request.method=="POST":
        subject_id = request.POST.get('subject_id','')
        module_id = request.POST.get('module_id','')
        if subject_id=='' or module_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            this_subject = Subject.objects.get(id=subject_id)
            module = Module.objects.get(id=module_id)
            module.subjects.add(this_subject)
            module.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def add_instructor_to_subject(request,subject_id):
    context = {}
    context['user'] = request.user
    this_subject = Subject.objects.get(id=subject_id)
    context['subject'] = this_subject
    if request.method=="POST":
        subject_id = request.POST.get('subject_id','')
        instructor_id = request.POST.get('instructor_id','')
        if instructor_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            instructor = User.objects.get(id=instructor_id)
            this_subject.instructors.add(instructor)
            this_subject.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['users'] = User.objects.all()
        context['subject_instructors'] = this_subject.instructors.all()
        return render_to_response('add_instructor_to_subject.html', context, RequestContext(request,context))


def get_description_of_outcome(request,outcome_id):
    if request.POST:
        outcome = Outcome.objects.get(id=outcome_id)
        outcome_description = outcome.description
        to_json = {
            'result': 'succeeded',
            'description': outcome_description,
        }
        return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def get_description_of_module(request,module_id):
    if request.POST:
        module = Module.objects.get(id=module_id)
        module_description = module.description
        to_json = {
            'result': 'succeeded',
            'description': module_description,
        }
        return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def get_description_of_subject(request,subject_id):
    if request.POST:
        subject = Subject.objects.get(id=subject_id)
        subject_description = subject.description
        to_json = {
            'result': 'succeeded',
            'description': subject_description,
            'name': str(subject.number).ljust(8)+subject.name, 
        }
        return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

def add_prereq_to_subject(request,subject_id):
    context = {}
    context['user'] = request.user
    this_subject = Subject.objects.get(id=subject_id)
    context['subject'] = this_subject
    if request.method=="POST":
        subject_id = request.POST.get('subject_id','')
        prereq_number = request.POST.get('prereq_number','')
        prereq_name = request.POST.get('prereq_name','')
        prereq_description = request.POST.get('prereq_description','')
        prereq_creator_id = request.POST.get('prereq_creator_id','')
        if prereq_number=='' or prereq_name=='' or prereq_description=='' or prereq_creator_id=='' or subject_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            prereq_creator = User.objects.get(id=prereq_creator_id)
            prereq = Subject(number=prereq_number,name=prereq_name,description=prereq_description,creator=prereq_creator)
            prereq.save()
            prereq.instructors.add(prereq_creator)
            this_subject.prerequisites.add(prereq)
            this_subject.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
    else:
        context['subjects'] = Subject.objects.all()
        context['subject_prereqs'] = this_subject.prerequisites.all()
        return render_to_response('add_prereq_to_subject.html', context, RequestContext(request,context))

def add_existing_prereq_to_subject(request,subject_id,prereq_id):
    if request.method=="POST":
        subject_id = request.POST.get('subject_id','')
        prereq_id = request.POST.get('prereq_id','')
        if subject_id=='' or prereq_id=='':
            to_json = {
                'result': 'failed'
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")
        else:
            this_subject = Subject.objects.get(id=subject_id)
            prereq = Subject.objects.get(id=prereq_id)
            this_subject.prerequisites.add(prereq)
            this_subject.save()
            to_json = {
                'result': 'succeeded',
            }
            return HttpResponse(simplejson.dumps(to_json), content_type="application/json")

