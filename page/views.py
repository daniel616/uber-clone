from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def index(request):
   # return HttpResponse("heh")
    return render(request,'page/index.html')
def rides(request):
    return render(request,'page/all_rides.html')
