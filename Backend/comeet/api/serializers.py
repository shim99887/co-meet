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
        fields = ('date',
                  'per_time',
                  'age_range',
                  'sex',
                  'city',
                  'gugun',
                  'popl')


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
