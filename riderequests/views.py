from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Request

from django.template import loader
from datetime import datetime

def index(request):
    all_requests = Request.objects.all()
    context = {
            'requests' : all_requests
        }
    template = loader.get_template('riderequests/index.html')

    return HttpResponse(template.render(context,request))

def newrequest(request):
    fields = request.POST
    t = datetime.now()
    q = Request(requester=fields['requester'], arrive_time=datetime.now(), request_time = datetime.now(), src_loc=fields['src_loc'], dst_loc=fields['dst_loc'])
    q.save()
    return HttpResponseRedirect(reverse('riderequests:index'))


def makerequest(request):
    template = loader.get_template('riderequests/makerequest.html')
    return HttpResponse(template.render({},request))
# Create your views here.
