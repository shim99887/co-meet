
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    url(r'^user$', views.User_list),
    url(r'^user/checkemail', views.check_email),
]
