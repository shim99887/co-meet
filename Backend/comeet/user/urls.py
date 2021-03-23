
from django.urls import path, include
from django.conf.urls import url
from .views import UserViewSet, EmailViewSet
# from . import views

urlpatterns = [

    path('', UserViewSet.as_view(
        {"get": "list", "post": "add_User"}), name="User"),
    path('(?P<username>[\w.@+-]+)/$', EmailViewSet.as_view(
        {"get": "email_vaild_check"}), name="Email"),
    # path('nickname', NicknameViewSet.as_view(
    #     {"get": "Nickname_vaild_check"}), name="Nickname"),
    # path("''/<string:email>",
    #      UserViewSet.as_view({"get": "list"}), name="email"),
]
