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


#import jwt
import json
from .token import user_activation_token
from .text import message
from comeet.settings import SECRET_KEY, EMAIL
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
        # print(request.data['email'])
        Users = User.objects.filter(email=request.data['email'])
        # if Users.exists():
        #     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        User_serializer = UserSerializer(data=request.data, partial=True)

        if not User_serializer.is_valid():
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        Users = User_serializer.save()

        current_site = get_current_site(request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(request.data['email']))
        token = user_activation_token.make_token(User)
        message_data = message(domain, uidb64, token)

        mail_title = "이메일 인증을 완료해주세요"
        mail_to = request.data['email']
        email = EmailMessage(mail_title, message_data, to=[mail_to])
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


# def send_email(request):
#     subject = "message"
#     to = ["dhpassion@naver.com"]
#     from_email = "comeetmanager@gmail.com"
#     message = "메시지 테스트"
#     EmailMessage(subject=subject, body=message,
#                  to=to, from_email=from_email).send()


def message(domain, uidb64, token):
    return f"아래 링크를 클릭하면 회원가입 인증이 완료됩니다.\n\n회원가입 링크 : http://{domain}/account/activate/{uidb64}/{token}\n\n감사합니다."


class Activate(viewsets.GenericViewSet,
               mixins.ListModelMixin,
               View):
    serializer_class = UserSerializer

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=email)

            if user_activation_token.check_token(user, token):
                user.is_auth = True
                user.save()

                return redirect(EMAIL['REDIRECT_PAGE'])

            return JsonResponse({"message": "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)
