from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from api.models import Code, Fpopl, Card, CoronaData
from .serializers import CodeSerializer, FpoplSerializer, CardSerializer, CoronaDataSerializer
from django.core.cache import cache
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
import io
import urllib, base64
# Create your views here.


class CoronaSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CoronaDataSerializer

    def set_corona(self, *args, **kwargs):
        # queryset data 받기
        corona_data = CoronaData.objects.all()
        if not corona_data.exists():
            raise HttpResponse()

        # json 파일로 변환
        corona_data_list = serializers.serialize('json', corona_data)
        # # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("corona_data", corona_data, 24 * 60 * 60)

        return JsonResponse({"message": "CORONA_SUCCESS"}, status=200)


class CodeSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CodeSerializer

    def set_code(self, *args, **kwargs):
        code_data = Code.objects.all()

       # json 파일로 변환
        code_data_list = serializers.serialize('json', code_data)
        # # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("code_data", code_data, 24 * 60 * 60)

        return JsonResponse({'message': 'CODE_SUCCESS'}, status=200)


class FpoplSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = FpoplSerializer

    def set_fpopl(self, *args, **kwargs):
        fpopl_data = Fpopl.objects.all()

       # json 파일로 변환
        fpopl_data_list = serializers.serialize('json', fpopl_data)
        # # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("fpopl_data", fpopl_data, 24 * 60 * 60)

        return JsonResponse({'message': 'FPOPL_SUCCESS'}, status=200)


class CoronaList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CoronaDataSerializer

    def get_corona_list(self, request, *args, **kwargs):
        corona_queryset = cache.get("corona_data")

        # 구군마다 전체 분포표 
        df = pd.DataFrame(list(corona_queryset.all().values("serial_number", "gugun")))
        df = df.groupby(["gugun"], as_index=False).count()
        
        df = df.drop(index=[8, 26], axis=0) # 기타, 타시도 삭제

        corona_json = df.to_json(orient= "index", force_ascii=False)
        # print(type(corona_json))
        # return None
        return JsonResponse(corona_json, safe= False)

class FpoplList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    erializer_class = FpoplSerializer

    def get_fpopl_list(self, request, *args, **kwargs):
        fpopl_queryset = cache.get("fpopl_data")

        df = pd.DataFrame(list(fpopl_queryset.all().values("date", "gugun", "popl")))

        fpopl_json = df.to_json(orient= "index", force_ascii=False)
        
        return JsonResponse(fpopl_json, safe= False)
