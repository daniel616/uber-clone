from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.


class Ride(models.Model):
#    owner=models.ForeignKey(User, on_delete=models.DO_NOTHING)
 #   sharer=models.ForeignKey(User, on_delete=models.DO_NOTHING)
  #  driver=models.ForeignKey(User, on_delete=models.DO_NOTHING)
    destination=models.CharField(max_length=200)
    arrival_time=models.DateTimeField(default=datetime.now,blank=True)
    start_time=models.DateTimeField(default=datetime.now,blank=True)
    confirmed = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return "this is ride"
        
class Vehicle(models.Model):
    vehicle_type_registered = models.CharField(max_length=200, blank=True)
    license_plate_number = models.CharField(max_length=200, blank=True)
    max_capacity = models.IntegerField(default=4, blank=True)
   # driver = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    special_requests_driver = models.CharField(max_length=200, blank=True)
    def	__str__(self):
        return	"vehicle"+str(self.liccense_plate_number)
    
