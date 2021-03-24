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
        # 중구 데이터 출력 query가 utf-8 잘되었는지 확인
        # print(corona_queryset.filter(gugun="중구").values())

        # corona_json = serializers.serialize(
        #     'json', corona_queryset.filter(gugun="영등포구"), ensure_ascii=False)

        # response = JsonResponse(corona_json, safe= False)
        df = pd.DataFrame(list(corona_queryset.all().values("serial_number", "date", "gugun")))
        df = df.groupby(["gugun"], as_index=False).count()
        # print(df)
        
        df = df.drop(index=[8, 26], axis=0) # 기타, 타시도 삭제

        # 그래프 표현
        rc('font', family='Malgun Gothic')
        # 별도로, 폰트를 바꿀 경우 마이너스가 표시되지 않는 경우도 있는데 이를 막아주는 코드입니다.
        rc('axes', unicode_minus=False)

        chart = sns.barplot(x="gugun", y="serial_number", data=df)
        chart.set_xticklabels(chart.get_xticklabels(), rotation=45)
        plt.title("서울시 코로나 구/군별 코로나 확진자 수")
        plt.xlabel("서울시 구/군")
        plt.ylabel("감염자 수")
        # plt.show()
        fig = plt.gcf()
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        string = base64.b64encode(buf.read())
        uri = urllib.parse.quote(string)

        return render(request, 'home.html', {'data':uri})
        # return JsonResponse(corona_json, safe= False)