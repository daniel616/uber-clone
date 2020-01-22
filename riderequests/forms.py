from django.forms import ModelForm

from .models import Request


"""
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
    request_time = models.DateTimeField('request sent time')
    src_loc = models.CharField(max_length = 500)
    dst_loc = models.CharField(max_length = 500)
"""

class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['requester', 
                'src_loc', 
                'dst_loc', 
                'arrive_time',
                'n_passengers',
                'allow_strangers']
