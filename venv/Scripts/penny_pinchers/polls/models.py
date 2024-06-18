import datetime
from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    birth_year = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

class mCollection(models.Model):
    cName = models.CharField(max_length=200)
    cDate = models.DateTimeField("date published")
    @admin.display(
            boolean = True,
            ordering='cDate',
            description='Published recently?'
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.cDate <= now
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

class mEntry(models.Model):
    eCollection = models.ForeignKey(mCollection, on_delete=models.CASCADE)
    eName = models.CharField(max_length=200)
    eYear =  models.IntegerField(default=0)
    ePlace = models.CharField(max_length=200)
    eCountry = models.CharField(max_length=200)
    eQuality = models.CharField(max_length=10)
    eFront = models.ImageField(upload_to = 'static/media')
    eBack = models.ImageField(upload_to = 'static/media')
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

 
