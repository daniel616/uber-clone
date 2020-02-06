from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.core.exceptions import ObjectDoesNotExist
from .models import Request

from .forms import RequestForm, JoinRequestForm, DriverSearchRequestForm

from django.template import loader
from datetime import datetime

def index(request):
    context = {
            'requests' : Request.objects.all()
            }
    return render(request,"riderequests/show_requests.html",context=context)




def error_page(request,title="Invalid input", message="Invalid input"):
    context = {
            "title": title,
            "message": message
            }
    return render(request,"riderequests/invalid.html",context=context)



def edit_requests(http_request):
    user = get_user(http_request)
    if http_request.method == "POST":
        try:
            req = Request.objects.get(pk = http_request.POST['id'])
            assert req.requester == user and req.status == "O"
            form = RequestForm(http_request.POST,instance = req)
            form.save()
            return HttpResponseRedirect(reverse("riderequests:index"))

        except (AssertionError, ObjectDoesNotExist):
            return error_page(http_request)

    else:
        try:
            rid = http_request.GET['id']
            req = Request.objects.get(pk=rid)
            assert req.requester==user and req.status=='O'
            form = RequestForm(instance = req)
            return render(http_request,"riderequests/make_edit.html",context = {"form":form, "id": rid})
        except (AssertionError, ObjectDoesNotExist):
            return error_page(http_request)

def get_user(request):
    return request.user.username

def my_dashboard(request):
    user = get_user(request)
    owned_requests = Request.objects.filter(requester__exact = user)
    provided_rides = Request.objects.filter(driver__exact = user)
    shared_requests = Request.objects.filter(other_user_passengers__contains = user)
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
            req.driver = get_user(request)
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
            req.other_user_passengers+='sd'
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
    q = Request(requester=get_user(request), arrive_time=datetime.now(), request_time = datetime.now(), src_loc=fields['src_loc'], dst_loc=fields['dst_loc'])
    q.save()
    return HttpResponseRedirect(reverse('riderequests:index'))


#http://blog.appliedinformaticsinc.com/using-django-modelform-a-quick-guide/
def specifyrequest(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            n_req = form.save(commit = False)
            
            n_req.requester = get_user(request)
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
