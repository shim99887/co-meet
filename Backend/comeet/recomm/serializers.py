from rest_framework import serializers
from recomm.models import DistWeight, CoronaWeight, FpoplWeight, DistanceData

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
