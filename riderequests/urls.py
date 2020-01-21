from django.urls import path

from . import views

app_name = 'riderequests'

urlpatterns = [ 
        path('',views.index, name = 'index'),
        path('newrequest/', views.newrequest, name = 'newrequest'),
        path('makerequest/',views.makerequest, name = 'makerequest'),
]
