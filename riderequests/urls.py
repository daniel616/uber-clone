from django.urls import path

from . import views

app_name = 'riderequests'

urlpatterns = [ 
        path('',views.index, name = 'index'),
        #path('newrequest/', views.newrequest, name = 'newrequest'),
        path('specifyrequest/',views.specifyrequest, name = 'specifyrequest'),
        path('joinrequest/', views.avail_for_share, name= 'joinrequest'),
        path('search_shareable_rides/', views.search_shareable_rides, name = 'search_shareable_rides'),
        path('driver_search_requests/', views.driver_search_requests, name = 'driver_search_requests'),
        path('give_ride/',views.driver_choose_requests, name = 'driver_choose_requests'),
        path('my_dashboard/', views.my_dashboard, name = 'my_dashboard'),
        path('edit_requests/', views.edit_requests, name = 'edit_requests'),
]
