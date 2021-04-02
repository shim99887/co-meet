from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from user.models import User, SearchLog
from .serializers import UserSerializer, UserBodySerializer, SearchLogSerializer, SearchLogBodySerializer
from drf_yasg.utils import swagger_auto_schema
from django.core import serializers

import jwt
import json
import bcrypt
from .token import user_activation_token
from .text import message
from comeet.settings import SECRET_KEY, REDIRECT_PAGE
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.core.cache import cache


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
        Users = User.objects.filter(email=request.data['email'])

        password = request.data['password'].encode('utf-8')
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
        password_crypt = password_crypt.decode('utf-8')

        request.data['password'] = password_crypt
        User_serializer = UserSerializer(data=request.data, partial=True)

        if not User_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        Users = User_serializer.save()

        domain = "j4a203.p.ssafy.io"
        uidb64 = urlsafe_base64_encode(force_bytes(request.data['email']))
        token = user_activation_token.make_token(Users)
        message_data = message(domain, uidb64, token)

        mail_title = "이메일 인증을 완료해주세요"
        mail_to = request.data['email']
        email = EmailMessage(subject=mail_title,
                             body=message_data, to=[mail_to])
        email.send()

        return Response(UserSerializer(User).data, status=status.HTTP_201_CREATED)


class EmailViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   View):

    serializer_class = UserSerializer

    def email_vaild_check(self, *args, **kwargs):

        Emails = User.objects.filter(email=self.kwargs['email'])

        if Emails.exists():
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


def message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/user/activate/{uidb64}/{token}\n\n감사합니다."


class Activate(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               View):
    serializer_class = UserSerializer

    def get(self, request, uidb64, token):
        try:
            email = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(email=email)
            if user_activation_token.check_token(user, token):
                user.is_auth = True
                user.save()

                return redirect(REDIRECT_PAGE)

            return JsonResponse({"message": "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


class LoginViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   View):

    @swagger_auto_schema(request_body=UserBodySerializer)
    def login_check(self, request):

        Users = User.objects.filter(email=request.data['email'])

        password = request.data['password'].encode('utf-8')

        if bcrypt.checkpw(password, Users[0].password.encode('utf-8')):

            token = jwt.encode(
                {'email': request.data['email']}, SECRET_KEY, algorithm="HS256")

            cache.set(request.data['email'], token, 60*60)

            return Response({"email": Users[0].email, "nickname": Users[0].nickname, "token": token}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    View):

    def logout_check(self, *args, **kwargs):

        cache.delete(self.kwargs['email'])

        return Response(True, status=status.HTTP_200_OK)


class SearchLogViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       View):
    serializer_class = SearchLogSerializer

    @swagger_auto_schema(request_body=SearchLogBodySerializer)
    def saveSearchLog(self, request):

        sl_serializer = SearchLogSerializer(data=request.data, partial=True)
        if not sl_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        sl_serializer.save()

        # 10개가 넘으면 처리를 여기서 할거
        searchLog = SearchLog.objects.filter(email=request.data['email'])
        searchLog_list = list(searchLog)

        if searchLog.count() > 10:
            eraseCount = searchLog.count() - 10
            for i in range(eraseCount):
                searchLog[i].delete()

        return Response(status=status.HTTP_200_OK)

    def serveSearchLog(self, *args, **kwargs):
        Search = SearchLog.objects.filter(email=self.kwargs['email'])
        search_list = serializers.serialize('json', Search)

        return HttpResponse(search_list, status=status.HTTP_200_OK)
