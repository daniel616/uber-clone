from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Request

from .forms import RequestForm, JoinRequestForm, DriverSearchRequestForm

from django.template import loader
from datetime import datetime

def index(request):
    all_requests = Request.objects.all()
    context = {
            'requests' : all_requests
            }
    template = loader.get_template('riderequests/show_requests.html')


    return HttpResponse(template.render(context,request))

def edit_requests(http_request):
    pass

def my_dashboard(request):
    owned_requests = Request.objects.filter(requester__exact = 'default_user')
    provided_rides = Request.objects.filter(driver__exact = 'default_user')
    shared_requests = Request.objects.filter(other_user_passengers__contains = 'default_user')
    ctx = {'owned_requests':owned_requests, 'provided_rides': provided_rides,
            'shared_requests':shared_requests}
    template = loader.get_template('riderequests/my_dashboard.html')

    return HttpResponse(template.render(ctx,request))


def driver_choose_requests(request):
    def make_form(request,prev_invalid_post):
        matches = Request.objects.filter(status__exact = 'O')
        if request.GET['src_loc']:
            matches = matches.filter(src_loc__exact = request.GET['src_loc'])
        if request.GET['dst_loc']:
            matches = matches.filter(dst_loc__exact = request.GET['dst_loc'])
        if request.GET['min_arrive_time']:
            matches = matches.filter(arrive_time__gte = request.GET['min_arrive_time'])
        if request.GET['max_arrive_time']:
            matches = matches.filter(arrive_time__lte = request.GET['max_arrive_time'])
        ctx = {
                'requests': matches,
                'invalid' : prev_invalid_post,
                }
        
        template = loader.get_template('riderequests/driver_pick_requests.html')
        return HttpResponse(template.render(ctx,request))

    if request.method == "POST":
        if request.POST['choice']:
            req = Request.objects.get(pk=request.POST['choice'])
            req.driver = "default_user"
            req.status = "C"
            req.save()
            return HttpResponseRedirect(reverse('riderequests:index'))
        else:
            return make_form(request,True)

        
    elif DriverSearchRequestForm(request.GET).is_valid():
        return make_form(request,False)
    else:
        return driver_search_requests(request,True)


def avail_for_share(request): 
    def make_form(request, prev_invalid_post):
        matches = Request.objects.filter(status__exact='O')
        matches = matches.filter(src_loc__exact=request.GET['src_loc'])
        matches = matches.filter(dst_loc__exact=request.GET['dst_loc'])
        matches = matches.filter(n_passengers__lt=str(4-int(request.GET['n_passengers'])))
        matches = matches.filter(allow_strangers__exact='True')

        context = {
                'requests' : matches,
                'invalid' : prev_invalid_post
                }

        template = loader.get_template('riderequests/join_requests.html')

        return HttpResponse(template.render(context,request))


    if request.method == "GET":
        if JoinRequestForm(request.GET).is_valid():
            return make_form(request,False)
        else:
            return HttpResponseRedirect(reverse('riderequests:search_shareable'))

    elif request.method == "POST":
        if request.POST['choice']:
            req = Request.objects.get(pk=request.POST['choice'])
            req.n_passengers += int(request.GET['n_passengers'])
            req.other_user_passengers+="default_user"
            req.save()
            return HttpResponseRedirect(reverse('riderequests:index'))
        else:
            return make_form(request,True)
    else:
        raise AssertionError('unrecognized method')

def search_shareable_rides(request):
    def produce_form(request,prev_invalid):
        context = {"invalid": prev_invalid, "form": JoinRequestForm()}
        template = loader.get_template('riderequests/search_shareable.html')
        return HttpResponse(template.render(context,request))
    
    return produce_form(request,False)

def driver_search_requests(request,prev_invalid_query=False):
    template = loader.get_template('riderequests/driver_search_req.html')
    ctx = {"form":DriverSearchRequestForm(), "invalid": prev_invalid_query}
    return HttpResponse(template.render(ctx,request))

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
            form = RequestForm()
            template = loader.get_template('riderequests/specifyrequest.html')
            return HttpResponse(template.render({'form':form,'invalid':True},request))

    else:
        form = RequestForm()

        template = loader.get_template('riderequests/specifyrequest.html')
        return HttpResponse(template.render({'form':form},request))


# Create your views here.
