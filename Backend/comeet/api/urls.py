from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from .views import CoronaSet, CodeSet, FpoplSet, CoronaList, FpoplList, FindLoc2, DataAnalysis, CoronaDataAnalysis

urlpatterns = [
    # path('', views.index, name='index'),
    # url(r'^code$', views.Code_list),
    # url(r'^fpopl$', views.Fpopl_list),
    # url(r'^coronaData$', views.CoronaData_list),
    path("corona", CoronaSet.as_view({"get": "set_corona"})),
    path("code", CodeSet.as_view({"get": "set_code"})),
    path("fpopl", FpoplSet.as_view({"get": "set_fpopl"})),
    path("corona-list", CoronaList.as_view({"get": "get_corona_list"})),
    path("fpopl-list", FpoplList.as_view({"get": "get_fpopl_list"})),
    path("recomm", FindLoc2.as_view({"post": "recomm_loc"})),
    path("data-analysis", DataAnalysis.as_view({"get": "data_analysis"})),
    path("corona-data-analysis",
         CoronaDataAnalysis.as_view({"get": "corona_data_analysis"})),
    # path("code", CodeSet.as_view({"get" : "list"})),
    # path("fpopl", FpoplSet.as_view({"get" : "list"})),
]
