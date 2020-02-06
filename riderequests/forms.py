from django.forms import ModelForm, Form
from django import forms
from .models import Request

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
                'allow_strangers']
   
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


