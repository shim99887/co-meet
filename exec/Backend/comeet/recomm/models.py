from djongo import models

class DistWeight(models.Model):
    signgu_nm = models.CharField(primary_key=True, max_length=20)
    weight_point = models.FloatField()

class CoronaWeight(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    signgu_nm = models.CharField(max_length=20)
    weight_point = models.FloatField()

class FpoplWeight(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    signgu_nm = models.CharField(max_length=20)
    weight_point = models.FloatField()

class DistanceData(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    signgu_nm = models.CharField(max_length=20)
    dist_weights = models.ArrayField(
        model_container=DistWeight
    )