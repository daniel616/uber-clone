from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('rides',views.rides,name='all_rides')
]
