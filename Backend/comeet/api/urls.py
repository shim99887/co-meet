
from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^code$', views.Code_list),
    url(r'^fpopl$', views.Fpopl_list),
    url(r'^coronaData$', views.CoronaData_list),
]
