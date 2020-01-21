from django.db import models


class Request(models.Model):
    requester = models.CharField(max_length=50)
    arrive_time = models.DateTimeField('expected arrival')
    request_time = models.DateTimeField('request sent time')
    src_loc = models.CharField(max_length = 500)
    dst_loc = models.CharField(max_length = 500)

    def __str__(self):
        return f"requester : {self.requester}, src: {self.src_loc}, dst: {self.dst_loc}"

# Create your models here.
