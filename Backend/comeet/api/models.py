from django.db import models

# Create your models here.


class Code(models.Model):
    _id = models.IntegerField(primary_key=True)
    adstrd_code = models.CharField(max_length=20)
    adstrd_nm = models.CharField(max_length=20)
    brtc_nm = models.CharField(max_length=20)
    signgu_nm = models.CharField(max_length=20)


class Fpopl(models.Model):
    _id = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=20)
    per_time = models.IntegerField()
    age_range = models.IntegerField()
    sex = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    gugun = models.CharField(max_length=10)
    popl = models.IntegerField()


class Card(models.Model):
    _id = models.IntegerField(primary_key=True)
    receipt_dttm = models.CharField(max_length=20)
    adstrd_code = models.CharField(max_length=20)
    adstrd_nm = models.CharField(max_length=20)
    mrhst_induty_cl_code = models.CharField(max_length=20)
    mrhst_induty_cl_nm = models.CharField(max_length=20)
    selng_cascnt = models.CharField(max_length=20)
    salamt = models.IntegerField()
