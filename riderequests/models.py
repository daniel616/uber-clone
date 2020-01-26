from django.db import models
import copy
from datetime import datetime

class Request(models.Model):
    OPEN = 'O'
    CONFIRMED = 'C'
    COMPLETED = 'F'
    STATUSES = (
            (OPEN, 'open'),
            (CONFIRMED, 'confirmed'),
            (COMPLETED, 'completed'),
    )

    requester = models.CharField(max_length=50)
    driver = models.CharField(max_length = 50, default = '')
    other_user_passengers =  models.CharField(max_length = 500, default = '')
    #TODO: fix these, should be linked to accounts somehow.
    status = models.CharField(
            max_length=1,
            choices = STATUSES,
            default = OPEN)

    n_passengers = models.IntegerField(default = 1)
    allow_strangers = models.BooleanField(default = False)

    arrive_time = models.DateTimeField('expected arrival')
    request_time = models.DateTimeField('request sent time',default = datetime.now)
    src_loc = models.CharField(max_length = 500)
    dst_loc = models.CharField(max_length = 500)

    def __str__(self):
        tmp = copy.copy(self.__dict__)
        del tmp['_state']
        return str(tmp)
# Create your models here.

class Vehicle(models.Model):
    vehicle_type_registered = models.CharField(max_length=200, blank=True)
    license_plate_number = models.CharField(max_length=200, blank=True)
    max_capacity = models.IntegerField(default=4, blank=True)
   # driver = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    special_requests_driver = models.CharField(max_length=200, blank=True)
    def	__str__(self):
        return	"vehicle"+str(self.liccense_plate_number)



