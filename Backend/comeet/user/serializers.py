from rest_framework import serializers
from user.models import User


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
