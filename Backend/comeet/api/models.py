from djongo import models

# Create your models here.


class Code(models.Model):
    _id = models.IntegerField(primary_key=True)
    adstrd_code = models.CharField(max_length=20)
    adstrd_nm = models.CharField(max_length=20)
    brtc_nm = models.CharField(max_length=20)
    signgu_nm = models.CharField(max_length=20)


class GugunLocate(models.Model):
    signgu_nm = models.CharField(max_length=20, primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()


class Gugun(models.Model):
    signgu_nm = models.CharField(max_length=20, primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()


class Fpopl(models.Model):
    _id = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=20)
    per_time = models.CharField(max_length=20)
    age_range = models.IntegerField()
    sex = models.CharField(max_length=10)
    city = models.CharField(max_length=10)
    gugun = models.CharField(max_length=10)
    popl = models.IntegerField()

class Fpopl_BC(models.Model):
    _id = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=20)
    per_time = models.CharField(max_length=20)
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


class CoronaData(models.Model):
    serial_number = models.IntegerField(primary_key=True)  # 연번
    patient_number = models.IntegerField()  # 환자 번호
    date = models.CharField(max_length=20)  # 확진 날짜
    gugun = models.CharField(max_length=20)  # 구, 군
    overseas = models.CharField(max_length=20)  # 해외 여부
    route = models.CharField(max_length=50)  # 확진 경로
    discharge = models.CharField(max_length=50, null=True)  # 퇴원 여부

class DistWegiht(models.Model):
    signgu_nm = models.CharField(max_length=20)
    weight_point = models.FloatField()

class CoronaWeight(models.Model):
    signgu_nm = models.CharField(max_length=20)
    weight_point = models.FloatField()

class FpoplWeight(models.Model):
    signgu_nm = models.CharField(max_length=20)
    weight_point = models.FloatField()

class RecommData(models.Model):
    signgu_nm = models.CharField(max_length=20)
    dist_weights = models.ArrayField(
        model_container= DistWegiht
    )
    corona_weights = models.ArrayField(
        model_container = CoronaWeight
    )
    fpopl_weights = models.ArrayField(
        model_container = FpoplWeight
    )
