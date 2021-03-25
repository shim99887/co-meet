from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from api.models import Code, Fpopl, Card, CoronaData, GugunLocate
from .serializers import CodeSerializer, FpoplSerializer, CardSerializer, CoronaDataSerializer, CodeBodySerializer
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rc
import io
import urllib
import base64
# 임시 함수(오늘 지울 것)
import random
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
        print("11")
        fpopl_data = Fpopl.objects.all()
        print("22")
       # json 파일로 변환
        fpopl_data_list = serializers.serialize('json', fpopl_data)
        # # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("fpopl_data", fpopl_data, 24 * 60 * 60)
        print("33")

        return JsonResponse({'message': 'FPOPL_SUCCESS'}, status=200)


class CoronaList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CoronaDataSerializer

    def get_corona_list(self, request, *args, **kwargs):
        corona_queryset = cache.get("corona_data")

        # 구군마다 전체 분포표
        df = pd.DataFrame(
            list(corona_queryset.all().values("serial_number", "gugun")))
        df = df.groupby(["gugun"], as_index=False).count()

        df = df.drop(index=[8, 26], axis=0)  # 기타, 타시도 삭제

        corona_json = df.to_json(orient="index", force_ascii=False)
        # print(type(corona_json))
        # return None
        return JsonResponse(corona_json, safe=False)


class FpoplList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = FpoplSerializer

    def get_fpopl_list(self, request, *args, **kwargs):

        # fpopl_queryset = cache.get("fpopl_data")
        # if fpopl_queryset is None :
        fpopl_queryset = Fpopl.objects.filter(date__contains="202001")

        df = pd.DataFrame(
            list(fpopl_queryset.all().values("date", "gugun", "popl")))

        # 일자별로 합쳐고 나눠 -> 하루동안 구별 평균 유동인구수
        # 예시) 20200101 , 영등포구 , popl 합 / 컬럼수
        # 월별로 합치고 일자로 나눠 -> 한달동안 구별 평균 유동인구수
        # 예시) 202001 동일하면 popl 합 / 컬럼수(일자별)
        # 한달, 구, 평균 유동인구수
        # 구로구 => 1월 ~ 12월 평균유동인구수
        # 구별로 유동인구수를 더하고 12로 나눠 그럼 1년동안 평균 유동인구수
        # 구별 평균 유동인구수를 한표에 보여줄수 있어 이게 정확해?
        #
        # print(df)
        fpopl_json = df.to_json(orient="index", force_ascii=False)
        print("333")
        return JsonResponse(fpopl_json, safe=False)
        # return None


class FindLoc(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CodeSerializer

    @swagger_auto_schema(request_body=CodeBodySerializer)
    def recomm_loc(self, request, *args, **kwargs):
        code_data = Code.objects.all()

        # 주어지는 주소 기반으로 중간지점을 가져오는 로직
        mid = midpoint(request.data['signgu_nm'])
        # 중간 지점을 기반으로 가까운 지역 리스트 조회
        nlist = nearbyArea(mid)
        # 로케이션 : lat , lng
        temp_area = random.choice(nlist)
        recomm_loc = GugunLocate.objects.filter(signgu_nm=temp_area)
        # 이지역의 코로나, 유동인구 제이슨 보내면 되는척가능

        # 해당 구의 위도 경도, 코로나 제이슨, 유동인구 제이슨

        # 코로나 제이슨, 유동인구 제이슨
        return JsonResponse({"recomm_loc": recomm_loc}, safe=False)


def midpoint(loc):
    return loc


def nearbyArea(loc):
    area = []
    code_list = Code.objects.filter(brtc_nm="서울특별시")
    for code in code_list.iterator():
        area.append(code.signgu_nm)
    area = list(set(area))
    print(area)
    return area
