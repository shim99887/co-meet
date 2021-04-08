from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
from .views import SaveDistWeight, SaveCoronaWeight, SaveFpoplWeight, RecommendPlace

urlpatterns = [
    path("dist", SaveDistWeight.as_view({"get": "save_dist_list"})),
    path("corona", SaveCoronaWeight.as_view({"get": "save_corona_weight"})),
    path("fpopl", SaveFpoplWeight.as_view({"get": "save_fpopl_weight"})),
    path("recommend", RecommendPlace.as_view({"post": "recommend"})),
]
