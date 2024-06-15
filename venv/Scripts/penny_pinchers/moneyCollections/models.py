import datetime

from django.db import models
from django.utils import timezone

class mCollection(models.Model):
    cName = models.CharField(max_length=200)
    cDate = models.DateTimeField("date published")
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.cDate <= now

class mEntry(models.Model):
    eCollection = models.ForeignKey(mCollection, on_delete=models.CASCADE)
    eName = models.CharField(max_length=200)
    eYear =  models.IntegerField(default=0)
    ePlace = models.CharField(max_length=200)
    eCountry = models.CharField(max_length=200)
    eQuality = models.CharField(max_length=10)
    eFront = models.ImageField(upload_to = 'media')
    eBack = models.ImageField(upload_to = 'media')

