from django.shortcuts import render,redirect
from djang.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("this is ride page")
