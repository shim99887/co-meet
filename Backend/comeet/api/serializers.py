from rest_framework import serializers
from api.models import Code, Fpopl, Card, CoronaData, GugunLocate, Gugun, Fpopl_BC, DistWeight, CoronaWeight, FpoplWeight, DistanceData


class CodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        fields = ('adstrd_code',
                  'adstrd_nm',
                  'brtc_nm',
                  'signgu_nm')


class CodeBodySerializer(serializers.Serializer):
    signgu_nm = serializers.CharField(help_text="구군이름")


class GugunLocateSerializer(serializers.ModelSerializer):

    class Meta:
        model = GugunLocate
        fields = ('signgu_nm', 'lat', 'lng')


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


class DistWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistWeight
        fields = ('signgu_nm', 'weight_point')


class CoronaWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoronaWeight
        fields = ('signgu_nm', 'weight_point')


class FpoplWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = FpoplWeight
        fields = ('signgu_nm', 'weight_point')


class DistanceDataSerializer(serializers.ModelSerializer):
    dist_weights = DistWeightSerializer(many=True, read_only=True)

    class Meta:
        model = DistanceData
        fields = ('signgu_nm', 'dist_weights')


class DistWeightBodySerializer(serializers.Serializer):
    signgu_nm = serializers.CharField(help_text="시군구 이름")
    weight = serializers.FloatField(help_text="거리 가중치")


class CoronaWeightBodySerializer(serializers.Serializer):
    signgu_nm = serializers.CharField(help_text="시군구 이름")
    weight = serializers.FloatField(help_text="코로나 지수 가중치")


class FpoplWeightBodySerializer(serializers.Serializer):
    signgu_nm = serializers.CharField(help_text="시군구 이름")
    weight = serializers.FloatField(help_text="유동인구 지수 가중치")


class DistanceDataBodySerializer(serializers.Serializer):
    signgu_nm = serializers.CharField(help_text="시군구 이름")
    dist_weights = DistWeightBodySerializer(many=True)
