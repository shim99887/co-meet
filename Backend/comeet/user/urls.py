
from django.urls import path, include
from django.conf.urls import url
from .views import UserViewSet, EmailViewSet
# from . import views

urlpatterns = [

    path('', UserViewSet.as_view(
        {"get": "list", "post": "add_User"}), name="User"),
    path('email', EmailViewSet.as_view(
        {"get": "email_vaild_check"}), name="Email"),
    # path("''/<string:email>",
    #      UserViewSet.as_view({"get": "list"}), name="email"),
]
