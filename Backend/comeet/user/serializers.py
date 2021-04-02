from rest_framework import serializers
from user.models import User, Search, SearchLog


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',
                  'password',
                  'nickname',
                  'is_auth')


class UserBodySerializer(serializers.Serializer):
    email = serializers.CharField(help_text="이메일")
    password = serializers.CharField(help_text="비밀번호")
    nickname = serializers.CharField(help_text="별명")
    is_auth = serializers.BooleanField(help_text="True, false")


class SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Search
        fields = ('juso', 'lat', 'lng')


class SearchLogSerializer(serializers.ModelSerializer):
    searchList = SearchSerializer(many=True)

    class Meta:
        model = SearchLog
        fields = ('email', 'searchList')


class SearchBodySerializer(serializers.Serializer):
    juso = serializers.CharField(help_text="주소")
    lat = serializers.FloatField(help_text="위도")
    lng = serializers.FloatField(help_text="경도")


class SearchLogBodySerializer(serializers.Serializer):
    email = serializers.CharField(help_text="이메일")
    SearchList = SearchBodySerializer(many=True)
