#from django.db import models
from djongo import models
# Create your models here.


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=30)
    password = models.CharField(max_length=70)
    nickname = models.CharField(max_length=30)
    is_auth = models.BooleanField(default=False)


class Search(models.Model):
    juso = models.CharField(primary_key=True, max_length=200)
    lat = models.FloatField()
    lng = models.FloatField()


class SearchLog(models.Model):
    email = models.CharField(max_length=200)
    searchList = models.ArrayField(
        model_container=Search
    )
