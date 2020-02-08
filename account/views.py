from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib import messages,auth

from riderequests.models import Request
from django.template import loader

# Create your views here.
def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'account/login.html')

        
def register(request):
    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password==password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'A user with this username already exists,please choose another username')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email account is associated with other account')
                    return redirect('login')
                else: 
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name,last_name=last_name)
                    user.save()
                    messages.success(request, 'Registration successful!')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords does not match, try again')
            return redirect('register')

    else:
        return render(request, 'account/register.html')

    
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/index')


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



def dashboard(request):
    
    return render(request,'account/dashboard.html')
