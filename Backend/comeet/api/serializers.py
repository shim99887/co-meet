from rest_framework import serializers
from api.models import Code, Fpopl, Card


class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        fields = ('adstrd_code',
                  'adstrd_nm',
                  'brtc_nm',
                  'signgu_nm')


class FpoplSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fpopl
        fields = ('일자',
                  '시간(1시간단위)',
                  '연령대(10세단위)',
                  '성별',
                  '시',
                  '군구',
                  '유동인구수')


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('receipt_dttm',
                  'adstrd_code',
                  'adstrd_nm',
                  'mrhst_induty_cl_code',
                  'mrhst_induty_cl_nm',
                  'selng_cascnt',
                  'salamt')
