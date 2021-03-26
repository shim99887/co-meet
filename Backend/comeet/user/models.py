from django.db import models

# Create your models here.


class User(models.Model):
    _id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=70)
    nickname = models.CharField(max_length=30)
    is_auth = models.BooleanField(default=False)
