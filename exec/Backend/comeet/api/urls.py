from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from .views import CoronaSet, FpoplSet, CoronaList, FpoplList, FpoplDataAnalysis, CoronaDataAnalysis

urlpatterns = [
    path("corona", CoronaSet.as_view({"get": "set_corona"})),
    path("fpopl", FpoplSet.as_view({"get": "set_fpopl"})),
    path("corona-list", CoronaList.as_view({"get": "get_corona_list"})),
    path("fpopl-list", FpoplList.as_view({"get": "get_fpopl_list"})),
    path("fpopl-data-analysis", FpoplDataAnalysis.as_view({"get": "fpopl_data_analysis"})),
    path("corona-data-analysis", CoronaDataAnalysis.as_view({"get": "corona_data_analysis"})),
]