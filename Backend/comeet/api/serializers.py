from rest_framework import serializers
from api.models import Code


class ApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Code
        fields = ('adstrd_code',
                  'adstrd_nm',
                  'brtc_nm',
                  'signgu_nm')
