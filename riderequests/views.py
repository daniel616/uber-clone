from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from .models import Request, Vehicle

from .forms import RequestForm, JoinRequestForm, DriverSearchRequestForm, VehicleForm
from django.template import loader
from datetime import datetime
import copy

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
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))

    if http_request.method == "POST":
        try:
            req = Request.objects.get(pk = http_request.POST['id'])
            assert req.requester == user and req.status == "O"
            form = RequestForm(http_request.POST,instance = req)
            form.save()
            return HttpResponseRedirect(reverse("riderequests:my_dashboard"))

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
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))



    def infer_allowed_statuses(request):
        if len(request.GET)==0:
            try:
                vehicle = Vehicle.objects.get(driver = user_object)
                return {"CONFIRMED":True, "OPEN": False, "COMPLETE": False}
            except ObjectDoesNotExist:
                return {"OPEN":True, "CONFIRMED": True, "COMPLETE":False}
        else:
            ret = {}
            for k in ['CONFIRMED','OPEN','COMPLETE']:
                ret[k] = True if k in request.GET else False
            return ret
            
            

    def get_allowed_reqs(allowed):
        ret = Request.objects.none()
        if allowed['CONFIRMED']:
            ret = ret|Request.objects.filter(status__exact='C')
        if allowed['OPEN']:
            ret = ret|Request.objects.filter(status__exact='O')
        if allowed['COMPLETE']:
            ret = ret|Request.objects.filter(status__exact = 'F')
        return ret
    allowed_statuses = infer_allowed_statuses(request)

    filtered_requests= get_allowed_reqs(allowed_statuses)
        
    
    owned_requests = [req_to_dict(obj) for obj in filtered_requests.filter(requester__exact = user)]
    provided_rides =  [req_to_dict(obj) for obj in filtered_requests.filter(driver__exact = user)]
    shared_requests =  [req_to_dict(obj) for obj in filtered_requests.filter(other_user_passengers__contains = user)]

    try:
        vehicle = Vehicle.objects.get(driver = user_object)
        vehicle = vehicle_to_dict(vehicle)
    except ObjectDoesNotExist:
        vehicle = None
    
    ctx = {'allowed_statuses':allowed_statuses,'owned_requests':owned_requests, 'provided_rides': provided_rides, 'shared_requests':shared_requests, 'vehicle':vehicle}
    

    return render(request,"riderequests/my_dashboard.html", context = ctx)


def req_to_dict(req_obj):
    tmp = copy.copy(req_obj.__dict__)
    del tmp['_state']
    stat_map = {"C":"CONFIRMED", "O": "OPEN", "F": "COMPLETE"}
    tmp['status'] = stat_map[tmp['status']]
    brand_map = {"L":"Lexus", "F": "Ferrari", "H":"Honda", '':''}
    tmp['vehicle_brand'] = brand_map[tmp['vehicle_brand']]
    return tmp

def vehicle_to_dict(vehicle_obj):
    tmp = copy.copy(vehicle_obj.__dict__)
    del tmp['_state']
    brand_map = {"L":"Lexus", "F": "Ferrari", "H":"Honda", '':''}
    tmp['vehicle_brand'] = brand_map[tmp['vehicle_brand']]
    return tmp


    

def remove_driver(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))

    try:
        uname = get_user(request)
        assert request.method == "POST"
        vehicle = Vehicle.objects.get(driver = User.objects.get(username = uname))
        vehicle.delete()
        return HttpResponseRedirect(reverse("riderequests:my_dashboard"))
    except:
        return render(request,"riderequests/invalid.html",context={"title":'Invalid request', "message":"Something went wrong. "})


def finish_ride(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))

    try:
        rid = request.POST['id']
        req = Request.objects.get(pk=rid)
        assert user == req.driver

        req.status = 'F'
        req.save()
        return HttpResponseRedirect(reverse("riderequests:my_dashboard"))
    except:
        return render(request,"riderequests/invalid.html",context={"title":'Invalid request', "message":"Something went wrong. "})



def driver_choose_requests(request):
    try:
        uname = get_user(request)
        u_obj = User.objects.get(username = uname)
        vehicle = Vehicle.objects.get(driver = u_obj)
    except:
        return HttpResponseRedirect(reverse('login'))
    
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
        
        matches = matches.filter(vehicle_brand__exact = '') | matches.filter(vehicle_brand__exact = vehicle.vehicle_brand)
        matches = matches.filter(special_features__exact = '') | matches.filter(special_features__exact = vehicle.special_features)
        

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
            req.license_plate = vehicle.license_plate
            notify_all_confirmed(req)
            req.save()
            return HttpResponseRedirect(reverse('riderequests:my_dashboard'))
        else:
            return make_form(request,True)

        
    elif DriverSearchRequestForm(request.GET).is_valid():
        return make_form(request,False)
    else:
        return driver_search_requests(request,True)

def notify_all_confirmed(c_req_obj):
    rider_unames = [c_req_obj.requester]
    rider_unames += c_req_obj.other_user_passengers.split(", ")
    rider_unames = filter(lambda x: x!='', rider_unames)
    rider_emails = [User.objects.get(username = u).email for u in rider_unames]

    driver_email = [User.objects.get(username = c_req_obj.driver).email]

    send_mail('Your ride has been confirmed', f'Hi! This is just to let you know that your ride info has been confirmed. Details below: \n{c_req_obj}',settings.EMAIL_HOST_USER, rider_emails)
    send_mail('You are giving a ride!', f'Hi! You have confirmed a ride request. Details below:\n{c_req_obj}', settings.EMAIL_HOST_USER, driver_email)



def avail_for_share(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))

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
            return HttpResponseRedirect(reverse('riderequests:search_shareable_rides'))

    elif request.method == "POST":
        if request.POST['choice']:
            req = Request.objects.get(pk=request.POST['choice'])
            req.n_passengers += int(request.GET['n_passengers'])
            req.other_user_passengers+= f',{get_user(request)}'
            req.save()
            return HttpResponseRedirect(reverse('riderequests:my_dashboard'))
        else:
            return make_form(request,True)
    else:
        raise AssertionError('unrecognized method')

def search_shareable_rides(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))
    context = {"form": JoinRequestForm()}
    return render(request,'riderequests/search_shareable.html',context = context)
    

    

def driver_search_requests(request,prev_invalid_query=False):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))
    ctx = {"form":DriverSearchRequestForm(), "invalid": prev_invalid_query}
    return render(request,'riderequests/driver_search_req.html', context = ctx)

def newrequest(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))
    fields = request.POST
    q = Request(requester=get_user(request), arrive_time=datetime.now(), request_time = datetime.now(), src_loc=fields['src_loc'], dst_loc=fields['dst_loc'])
    q.save()
    return HttpResponseRedirect(reverse('riderequests:my_dashboard'))

def specify_vehicle(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))






    def get_v_form(u_obj):
        try:
            vehicle = Vehicle.objects.get(driver = user_object)
            form = VehicleForm( instance = vehicle)
        except ObjectDoesNotExist:
            form = VehicleForm()
        return form

    if request.method == "POST":
        try:
            vehicle = Vehicle.objects.get(driver = user_object)
            form = VehicleForm(request.POST, instance = vehicle)
        except ObjectDoesNotExist:
            form = VehicleForm(request.POST)
        
        
        if form.is_valid():
            vehicle = form.save(commit = False)
            vehicle.driver = user_object
            vehicle.save()
            return HttpResponseRedirect(reverse('riderequests:my_dashboard'))

        else:
            context = {"form":form, 'title':'Specify vehicle', 'invalid':True}
            return render(request,'riderequests/default_form.html', context = context)
    else:
        form = get_v_form(user_object)
        return render(request, 'riderequests/default_form.html', context = {"form":form, 'title':
            'Specify vehicle'})

    

#http://blog.appliedinformaticsinc.com/using-django-modelform-a-quick-guide/
def specifyrequest(request):
    try:
        user = get_user(request)
        user_object = User.objects.get(username = user)
    except ObjectDoesNotExist:
        messages.error(request,"login first!")
        return HttpResponseRedirect(reverse("login"))

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            n_req = form.save(commit = False)
            
            n_req.requester = get_user(request)
            n_req.request_time = datetime.now()
            n_req.save()
            return HttpResponseRedirect(reverse('riderequests:my_dashboard'))
        else:
            form = RequestForm()
            template = loader.get_template('riderequests/specifyrequest.html')
            return HttpResponse(template.render({'form':form,'invalid':True},request))

    else:
        form = RequestForm()

        template = loader.get_template('riderequests/specifyrequest.html')
        return HttpResponse(template.render({'form':form},request))


# Create your views here.
