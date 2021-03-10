from django.db import models

# Create your models here.


class Code(models.Model):
    _id = models.IntegerField(primary_key=True)
    adstrd_code = models.CharField(max_length=20)
    adstrd_nm = models.CharField(max_length=20)
    brtc_nm = models.CharField(max_length=20)
    signgu_nm = models.CharField(max_length=20)

    # @property
    # def code_list(self):
    #     return self.category.split("|") if self.category else []
    # class Meta:
    #     # abstract = True  # sqlite3 사용 시 어째선지 이게 있으면 마이그레이션이 안 됨.
    #     managed = True
    #     db_table = 'adstrd_master'
    #     app_label = 'api'
    #     ordering = ['_id', ]
    #     verbose_name_plural = '행정동코드'
