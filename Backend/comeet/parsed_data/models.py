from django.db import models

# Create your models here.

class CoronaData(models.Model) :
    _id = models.IntegerField(primary_key=True) # 연번 
    patient_number = models.IntegerField() # 환자 번호
    date = models.CharField(max_length = 20)# 확진 날짜
    dong = models.CharField(max_length = 20)# 동 
    overseas = models.CharField(max_length = 20)# 해외 여부 
    route = models.CharField(max_length = 50)# 확진 경로
    discharge = models.CharField(max_length = 50, null=True)# 퇴원 여부
    