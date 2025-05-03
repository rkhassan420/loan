from django.db import models
import datetime

class Qist(models.Model):
    sr=models.IntegerField(default=0)
    date = models.DateField(default=datetime.date.today)
    amount=models.IntegerField( default=0)
    t_id=models.IntegerField(default=0)
    sender=models.CharField(max_length=100,default=0)
    receiver=models.CharField(max_length=100,default=0)


    