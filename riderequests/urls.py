from django.urls import path

from . import views

app_name = 'riderequests'

urlpatterns = [ 
        path('',views.index, name = 'index'),
        #path('newrequest/', views.newrequest, name = 'newrequest'),
        path('specifyrequest/',views.specifyrequest, name = 'specifyrequest'),
        path('joinrequest/', views.avail_for_share, name= 'joinrequest')
]
