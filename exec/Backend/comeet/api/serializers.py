from rest_framework import serializers
from api.models import Fpopl, CoronaData, Gugun, Fpopl_BC

class GugunSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gugun
        fields = ('signgu_nm', 'lat', 'lng')


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


class Fpopl_BCSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fpopl_BC
        fields = ('date',
                  'per_time',
                  'age_range',
                  'sex',
                  'city',
                  'gugun',
                  'popl')

class CoronaDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CoronaData
        fields = ('serial_number',
                  'patient_number',
                  'date',
                  'gugun',
                  'overseas',
                  'route',
                  'discharge')