from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Request

from .forms import RequestForm

from django.template import loader
from datetime import datetime

def index(request):
    all_requests = Request.objects.all()
    context = {
            'requests' : all_requests
        }
    template = loader.get_template('riderequests/show_requests.html')

    return HttpResponse(template.render(context,request))

def avail_for_share(request):
    invalid = False
    if request.method == "POST":
        req = Request.objects.get(pk=request.POST['choice'])
        req.n_passengers += 1
        req.other_user_passengers+="apassenger"
        req.save()
        return HttpResponseRedirect(reverse('riderequests:index'))
    else:
        invalid = True

    avail = Request.objects.filter(allow_strangers=True)
    context = {
            'requests' : avail,
            'invalid' : invalid
            }

    template = loader.get_template('riderequests/join_requests.html')

    return HttpResponse(template.render(context,request))


def newrequest(request):
    fields = request.POST
    t = datetime.now()
    q = Request(requester=fields['requester'], arrive_time=datetime.now(), request_time = datetime.now(), src_loc=fields['src_loc'], dst_loc=fields['dst_loc'])
    q.save()
    return HttpResponseRedirect(reverse('riderequests:index'))


#http://blog.appliedinformaticsinc.com/using-django-modelform-a-quick-guide/
def specifyrequest(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            n_req = form.save(commit = False)
            n_req.request_time = datetime.now()
            n_req.save()
            return HttpResponseRedirect(reverse('riderequests:index'))
        else:
            import pdb; pdb.set_trace()
            form = RequestForm()
            template = loader.get_template('riderequests/specifyrequest.html')
            return HttpResponse(template.render({'form':form,'invalid':True},request))
    
    else:
        form = RequestForm()

        template = loader.get_template('riderequests/specifyrequest.html')
        return HttpResponse(template.render({'form':form},request))
# Create your views here.
