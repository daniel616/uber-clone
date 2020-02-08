from django.forms import ModelForm, Form
from django import forms
from .models import Request, Vehicle

from datetime import datetime, timedelta
from django.utils import timezone

class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = [
                'src_loc', 
                'dst_loc', 
                'arrive_time',
                'n_passengers',
                'allow_strangers',
                'vehicle_brand',
                'special_features']
   
def hour_from_now():
    d = timedelta(hours = 1)
    return timezone.now() + d


class JoinRequestForm(Form):
    src_loc = forms.CharField(label = 'src_loc', max_length=100, initial = '', required = False)
    dst_loc = forms.CharField(label = 'dst_loc', max_length =100, initial = '', required = False)
    min_arrive_time = forms.DateTimeField(label = 'minimum arrive time', initial = timezone.now, required = False)
    max_arrive_time = forms.DateTimeField(label = 'max arrivetime', initial = hour_from_now, required = False)
    n_passengers = forms.DecimalField(max_value = 4, min_value = 1, label = 'n_passengers', initial = 1)



class DriverSearchRequestForm(Form):
    src_loc = forms.CharField(label = 'src_loc', max_length=100, initial = '', required = False)
    dst_loc = forms.CharField(label = 'dst_loc', max_length =100, initial = '', required = False)
    min_arrive_time = forms.DateTimeField(label = 'minimum arrive time', initial = timezone.now, required = False)
    max_arrive_time = forms.DateTimeField(label = 'max arrivetime', initial = hour_from_now, required = False)


class VehicleForm(ModelForm):
    '''
    vehicle_type_registered = models.CharField(max_length=200, blank=True)
    vehicle_brand = models.CharField(max_length = 2, choices = BRANDS, default = HONDA)
    license_plate_number = models.CharField(max_length=200, blank=True)
    max_capacity = models.IntegerField(default=4, blank=True)
    driver = models.OneToOneField(User,on_delete = models.CASCADE, null=True)
    special_features = models.CharField(max_length=200, blank=True)

    '''
    
    class Meta:
        model = Vehicle
        fields = [
                'vehicle_brand',
                'license_plate_number',
                'max_capacity',
                'special_features',
                ]


