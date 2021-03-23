
from django.urls import path, include
from django.conf.urls import url
from .views import UserViewSet
# from . import views

urlpatterns = [

    path('', UserViewSet.as_view(
        {"get": "list", "post": "add"}), name="User"),
    # path("''/<string:email>",
    #      UserViewSet.as_view({"get": "list"}), name="email"),
]
