#!/usr/bin/python

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from models import Module

#-----------------------------------------------------------------------------
# index

@login_required
def index(request):
    context ={}
    latest_module_list = Module.objects.all().order_by('-date')[:10]
    user_module_list   = Module.objects.filter(creator=request.user).order_by('-date')[:5]
    return render_to_response('index.html', {'latest_module_list': latest_module_list, 'user_module_list': user_module_list})

def module(request, module_id):
    module = get_object_or_404(Module, mk=module_id)
    return render(request, 'module.html', {'module': module})
    


