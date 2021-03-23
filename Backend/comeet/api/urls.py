from django.urls import path, include
from django.conf.urls import url
from django.conf import settings 
from .views import CoronaSet, CodeSet, FpoplSet, CoronaList

urlpatterns = [
    # path('', views.index, name='index'),
    # url(r'^code$', views.Code_list),
    # url(r'^fpopl$', views.Fpopl_list),
    # url(r'^coronaData$', views.CoronaData_list),
    path("corona", CoronaSet.as_view({"get" : "list"})),
    path("code", CodeSet.as_view({"get" : "list"})),
    path("fpopl", FpoplSet.as_view({"get" : "list"})),
    path("corona-list", CoronaList.as_view({"get" : "list"})),
    # path("code", CodeSet.as_view({"get" : "list"})),
    # path("fpopl", FpoplSet.as_view({"get" : "list"})),
]

