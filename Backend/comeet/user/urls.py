
from django.urls import path, include
from django.conf.urls import url
from .views import UserViewSet, EmailViewSet, NickNameViewSet, Activate, LoginViewSet, LogoutViewSet, SearchLogViewSet

urlpatterns = [
    # get : User 전체 정보 조회, post : 회원가입 시 DB에 User 정보 추가.
    path('', UserViewSet.as_view(
        {"get": "list", "post": "add_User"}), name="User"),

    # get : 중복된 email 확인, delete : 회원 탈퇴 시 User 정보 추가.
    path('email/<email>', EmailViewSet.as_view(
        {"get": "email_vaild_check", "delete": "delete_user"}), name="Email"),

    # get : 중복된 Nickname 확인
    path('nickname/<nickname>', NickNameViewSet.as_view(
        {"get": "nickname_vaild_check"}), name="NickName"),

    # get : 이메일 인증 시 정상적인 Email token인지 확인.
    path('activate/<str:uidb64>/<str:token>',
         Activate.as_view({"get": "get"}), name="EmailAuthCheck"),

    # post : 아이디, 비밀번호 확인 후 로그인 처리.
    path('login', LoginViewSet.as_view(
        {"post": "login_check"}), name="Login"),

    # get : 해당 유저 로그아웃 처리.
    path('logout/<email>', LogoutViewSet.as_view(
        {"get": "logout_check"}), name="Logout"),

    # post : 유저가 검색한 로그 저장.
    path('searchlog', SearchLogViewSet.as_view(
         {"post": "saveSearchLog"}), name="saveSearchLog"),

    # get : 유저가 검색한 로그 조회.
    path('searchlog/<email>', SearchLogViewSet.as_view(
         {"get": "serveSearchLog"}), name="serveSearchLog")
]
