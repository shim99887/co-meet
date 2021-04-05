from django.core.cache import cache
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from comeet.settings import SECRET_KEY, REDIRECT_PAGE
from .text import message
from .token import user_activation_token
from django.core import serializers
import jwt
import json
import bcrypt

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.views import View
from user.models import User, SearchLog
from .serializers import UserSerializer, UserBodySerializer, SearchLogSerializer, SearchLogBodySerializer
from drf_yasg.utils import swagger_auto_schema
import pandas as pd


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  View):
    """
        User CRUD 관련 함수

        ---
        # 함수 설명
            - user_list : user 객체의 리스트를 리턴
            - add_User : 회원가입
    """
    serializer_class = UserSerializer   # 이 클래스형 view 에서 사용할 시리얼라이저를 선언

    def get_queryset(self):

        Users = User.objects.all()
        if not Users.exists():
            raise Http404()

        return Users

    @swagger_auto_schema(request_body=UserBodySerializer)   # post에만 붙일 수 있음.
    def add_User(self, request):
        Users = User.objects.filter(
            email=request.data['email'])    # 해당하는 이메일이 있는지 check

        password = request.data['password'].encode('utf-8')     # pwd 암호화.
        password_crypt = bcrypt.hashpw(password, bcrypt.gensalt())
        password_crypt = password_crypt.decode('utf-8')

        request.data['password'] = password_crypt
        User_serializer = UserSerializer(data=request.data, partial=True)

        if not User_serializer.is_valid():  # request data가 User_serializer에 맞는 form인지 확인.
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        Users = User_serializer.save()  # DB에 회원정보 저장.

        # token발급 후 사용자의 email로 보낼 링크 및 메세지 작성
        domain = "j4a203.p.ssafy.io"        # url중 host부분
        # email을 url로 안전하게 전달하기 위한 작업.
        uidb64 = urlsafe_base64_encode(force_bytes(request.data['email']))
        # User의 email token생성.
        token = user_activation_token.make_token(Users)
        message_data = message(domain, uidb64, token)   # email 인증 링크 생성.

        mail_title = "이메일 인증을 완료해주세요"   # email 내용 생성.
        mail_to = request.data['email']
        email = EmailMessage(subject=mail_title,
                             body=message_data, to=[mail_to])
        email.send()        # email 발송

        return Response(UserSerializer(User).data, status=status.HTTP_201_CREATED)


class EmailViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   View):
    """
        이메일 관련 함수

        ---
        # 함수 설명
            - email_vaild_check : 이메일 중복 체크 결과를 리턴하는 함수
            - delete_user : 해당 이메일에 해당하는 user 탈퇴
    """
    serializer_class = UserSerializer

    def email_vaild_check(self, *args, **kwargs):

        # 해당 email이 DB에 존재하는지 check
        Emails = User.objects.filter(email=self.kwargs['email'])

        if Emails.exists():     # 존재한다면 에러 status전달.
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(True, status=status.HTTP_200_OK)

    def delete_user(self, *args, **kwargs):

        # 삭제할 User의 email을 DB에서 조회.
        Emails = User.objects.filter(email=self.kwargs['email'])

        if not Emails.exists():     # 삭제할 User의 email이 없다면 에러 status전달.
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        # 사용자가 작성한 form이 email form이 아니라면 에러 status 전달.
        if not "@" in self.kwargs['email']:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        # DB에서 User의 email을 삭제.
        User.objects.filter(email=self.kwargs['email']).delete()

        return Response(True, status=status.HTTP_200_OK)


class NickNameViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      View):
    """
        닉네임 중복 체크 함수

        ---

    """
    serializer_class = UserSerializer

    def nickname_vaild_check(self, *args, **kwargs):

        # 사용자가 작성한 닉네임이 있는지 확인.
        NickNames = User.objects.filter(nickname=self.kwargs['nickname'])

        if NickNames.exists():      # DB에 해당 닉네임이 있다면 에러 status 전달.
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        return Response(True, status=status.HTTP_200_OK)


def message(domain, uidb64, token):     # 보낼 메세지 내용 생성 함수.
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/user/activate/{uidb64}/{token}\n\n감사합니다."


class Activate(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               View):
    """
        이메일 인증 토큰 validation 함수

        ---
    """
    serializer_class = UserSerializer

    def get(self, request, uidb64, token):
        try:
            # url에 담긴 암호화된 email정보 복호화 과정.
            email = force_text(urlsafe_base64_decode(uidb64))
            # 해당 email을 DB에서 조회
            user = User.objects.get(email=email)
            # token이 맞다면 auth값을 false->true로 변경.
            if user_activation_token.check_token(user, token):
                user.is_auth = True
                user.save()

                return redirect(REDIRECT_PAGE)

            # token이 맞지 않다면 해당 에러 status전달.
            return JsonResponse({"message": "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)


class LoginViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   View):
    """
        로그인 함수

        ---
    """
    @swagger_auto_schema(request_body=UserBodySerializer)
    def login_check(self, request):

        # 해당 email을 DB에서 조회.
        Users = User.objects.filter(email=request.data['email'])

        password = request.data['password'].encode(
            'utf-8')  # 암호화된 pwd와 비교하기 위해 암호화 작업

        # DB에 저장된 암호와 동일한지 판단.
        if bcrypt.checkpw(password, Users[0].password.encode('utf-8')):

            token = jwt.encode(     # email을 기준으로 jwt token생성.
                {'email': request.data['email']}, SECRET_KEY, algorithm="HS256")

            # redis에 60분동안 token저장.
            cache.set(request.data['email'], token, 60*60)

            return Response({"email": Users[0].email, "nickname": Users[0].nickname, "token": token}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    View):
    """
        로그아웃 함수

        ---
    """

    def logout_check(self, *args, **kwargs):

        cache.delete(self.kwargs['email'])  # redis에서 캐시 삭제

        return Response(True, status=status.HTTP_200_OK)


class SearchLogViewSet(viewsets.GenericViewSet,
                       mixins.ListModelMixin,
                       View):
    """
        검색 로그 관련 함수

        ---
        # 함수 설명
            - saveSearchLog : 검색 로그를 저장한다.
            - serveSearchLog : 이메일에 해당하는 검색 로그를 조회한다.
    """
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
        search_df = pd.DataFrame(
            data=list(Search.values('searchList'))).to_dict()

        return JsonResponse(search_df, status=status.HTTP_200_OK)
