
from django.urls import path, include
from django.conf.urls import url
from .views import UserViewSet, EmailViewSet, NickNameViewSet, Activate, LoginViewSet, LogoutViewSet, SearchLogViewSet
#from . import views

urlpatterns = [

    path('', UserViewSet.as_view(
        {"get": "list", "post": "add_User"}), name="User"),
    path('email/<email>', EmailViewSet.as_view(
        {"get": "email_vaild_check", "delete": "delete_user"}), name="Email"),
    path('nickname/<nickname>', NickNameViewSet.as_view(
        {"get": "nickname_vaild_check", "post": "change_nickname"}), name="NickName"),
    #path('send_email/', views.send_email, name='send_email'),
    path('activate/<str:uidb64>/<str:token>',
         Activate.as_view({"get": "get"})),

    path('login', LoginViewSet.as_view(
        {"post": "login_check"}), name="Login"),

    path('logout/<email>', LogoutViewSet.as_view(
        {"get": "logout_check"}), name="Logout"),

    path('searchlog', SearchLogViewSet.as_view(
         {"post": "saveSearchLog"}), name="saveSearchLog")
]
