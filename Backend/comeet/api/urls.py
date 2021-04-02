from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from .views import CoronaSet, CodeSet, FpoplSet, CoronaList, FpoplList, FindLoc, SaveDistWeight, SaveCoronaWeight, SaveFpoplWeight, DataAnalysis, CoronaDataAnalysis, RecommendPlace

urlpatterns = [
    path("corona", CoronaSet.as_view({"get": "set_corona"})),
    path("code", CodeSet.as_view({"get": "set_code"})),
    path("fpopl", FpoplSet.as_view({"get": "set_fpopl"})),
    path("corona-list", CoronaList.as_view({"get": "get_corona_list"})),
    path("fpopl-list", FpoplList.as_view({"get": "get_fpopl_list"})),
    path("search-recomm", FindLoc.as_view({"post": "recomm_loc"})),
    path("save-dist", SaveDistWeight.as_view({"get": "save_dist_list"})),
    path("save-corona",
         SaveCoronaWeight.as_view({"get": "save_corona_weight"})),
    path("save-fpopl", SaveFpoplWeight.as_view({"get": "save_fpopl_weight"})),
    path("data-analysis", DataAnalysis.as_view({"get": "data_analysis"})),
    path("corona-data-analysis",
         CoronaDataAnalysis.as_view({"get": "corona_data_analysis"})),
    path("recommend",
         RecommendPlace.as_view({"post": "recommend"})),
]
