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
    owner = models.CharField(max_length = 50)
    #TODO: fix me
