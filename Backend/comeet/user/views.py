from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
# from django.http.response import JsonResponse
from django.views import View
from user.models import User
from .serializers import UserSerializer, UserBodySerializer
from drf_yasg.utils import swagger_auto_schema


import jwt
import json
from .tokens import user_activation_token
from .text import message
from my_settings import SECRET_KEY, EMAIL
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  View):

    serializer_class = UserSerializer   # 이 클래스형 view 에서 사용할 시리얼라이저를 선언

    def get_queryset(self):

        Users = User.objects.all()
        if not Users.exists():
            raise Http404()

        return Users

    @swagger_auto_schema(request_body=UserBodySerializer)   # post에만 붙일 수 있음.
    def add_User(self, request):
        Users = User.objects.filter(**request.data.email)
        # if Users.exists():
        #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        User_serializer = UserSerializer(data=request.data, partial=True)
        if not User_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        Users = User_serializer.save()

        return Response(UserSerializer(User).data, status=status.HTTP_201_CREATED)


class EmailViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   View):

    serializer_class = UserSerializer

    def email_vaild_check(self, *args, **kwargs):

        Emails = User.objects.filter(email=self.kwargs['email'])

        if Emails.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        if not "@" in self.kwargs['email']:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(True, status=status.HTTP_200_OK)

    def delete_user(self, *args, **kwargs):

        Emails = User.objects.filter(email=self.kwargs['email'])

        if not Emails.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        if not "@" in self.kwargs['email']:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        User.objects.filter(email=self.kwargs['email']).delete()

        return Response(True, status=status.HTTP_200_OK)


class NickNameViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      View):

    serializer_class = UserSerializer

    def nickname_vaild_check(self, *args, **kwargs):

        NickNames = User.objects.filter(nickname=self.kwargs['nickname'])

        if NickNames.exists():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(True, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserBodySerializer)
    def change_nickname(self, request):

        return Response(True, status=status.HTTP_200_OK)


def send_email(request):
    subject = "message"
    to = ["dhpassion@naver.com"]
    from_email = "comeetmanager@gmail.com"
    message = "메시지 테스트"
    EmailMessage(subject=subject, body=message,
                 to=to, from_email=from_email).send()
