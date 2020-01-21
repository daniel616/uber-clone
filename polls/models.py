import datetime

from django.db import models
from django.utils import timezone



if __name__ == "__main__":
    from django.conf import settings

    settings.configure(DEBUG=True)
    import pdb; pdb.set_trace()

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text

    def was_published_recently(self):

        return timezone.now()>= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
# Create your models here.


    def __str__(self):
        return self.choice_text

