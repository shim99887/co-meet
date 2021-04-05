from rest_framework import status, viewsets, mixins
from django.views import View
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from api.models import Fpopl, CoronaData, Gugun, Fpopl_BC
from .serializers import FpoplSerializer, CoronaDataSerializer
from django.core.cache import cache
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from matplotlib import rc
import io
import urllib
import base64
from datetime import datetime, timedelta, date

class CoronaSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CoronaDataSerializer

    def set_corona(self, *args, **kwargs):
        # queryset data 받기
        corona_data = CoronaData.objects.all()
        if not corona_data.exists():
            raise HttpResponse()

        # json 파일로 변환
        corona_data_list = serializers.serialize('json', corona_data)
        # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("corona_data", corona_data, 24 * 60 * 60)

        return JsonResponse({"message": "CORONA_SUCCESS"}, status=200)

class FpoplSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = FpoplSerializer

    def set_fpopl(self, *args, **kwargs):
        # queryset data 받기
        fpopl_data = Fpopl.objects.all()
        # json 파일로 변환
        fpopl_data_list = serializers.serialize('json', fpopl_data)
        # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("fpopl_data", fpopl_data, 24 * 60 * 60)

        return JsonResponse({'message': 'FPOPL_SUCCESS'}, status=200)

class CoronaList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = CoronaDataSerializer

    def get_corona_list(self, request, *args, **kwargs):
        corona_queryset = CoronaData.objects.filter(date__contains="2021-03")

        # 구군마다 전체 분포표
        df = pd.DataFrame(
            list(corona_queryset.all().values("serial_number", "gugun")))
        df = df.groupby(["gugun"], as_index=False).count()

        df = df.drop(index=[8, 26], axis=0)  # 기타, 타시도 삭제

        corona_json = df.to_dict()

        return JsonResponse(corona_json, safe=False)

class FpoplList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = FpoplSerializer

    def get_fpopl_list(self, request, *args, **kwargs):

        fpopl_queryset = Fpopl.objects.filter(date__contains="202002")

        df = pd.DataFrame(
            list(fpopl_queryset.all().values("date", "gugun", "popl")))

        fpopl_json = df.to_json(orient="index", force_ascii=False)
        return JsonResponse(fpopl_json, safe=False)

class FpoplDataAnalysis(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def fpopl_data_analysis(self, *args, **kwargs):
        f_path = "c:/Windows/Fonts/malgun.ttf"
        font_name = fm.FontProperties(fname=f_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)

        bc_data = Fpopl_BC.objects.filter(age_range__in=[20, 30, 40])
        ac_data = Fpopl.objects.filter(age_range__in=[20, 30, 40])

        bc_df = pd.DataFrame(list(bc_data.values("date", "gugun", "popl")))
        ac_df = pd.DataFrame(list(ac_data.values("date", "gugun", "popl")))

        total_df = pd.concat([bc_df, ac_df], axis=0, ignore_index=True)

        raw_1 = total_df.groupby(by=['date', 'gugun']).sum().reset_index()

        raw_1["date"] = pd.to_datetime(raw_1["date"], format='%Y%m%d')

        # '연도', '월', '일' 컬럼 생성
        raw_1['year'] = raw_1.date.dt.year
        raw_1['month'] = raw_1.date.dt.month
        raw_1['day'] = raw_1.date.dt.day

        # 월평균 유동인구수 구하기
        temp = raw_1.groupby(
            by=["gugun", "year", "month"]).mean().reset_index()
        raw_1 = temp.drop('day', axis=1)

        # 그래프 그리기
        raw_1 = raw_1.set_index('gugun')

        fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(15, 15))

        for i, f in enumerate(raw_1.index.unique()):
            r = int(i / 5)  # 행별로 그래프 배치하기
            c = i % 5  # 열별로 그래프 배치하기
            df19 = raw_1[(raw_1.index == f) & (raw_1.year == 2019)]
            line19 = sns.lineplot(
                data=df19, x='month', y='popl', label='2019', ax=axes[r][c])
            df20 = raw_1[(raw_1.index == f) & (raw_1.year == 2020)]
            line20 = sns.lineplot(
                data=df20, x='month', y='popl', label='2020', ax=axes[r][c])
            df21 = raw_1[(raw_1.index == f) & (raw_1.year == 2021)]
            line21 = sns.lineplot(
                data=df21, x='month', y='popl', label='2021', ax=axes[r][c])
            line21.set_ylim(0, 1.5e+07)
            line21.set_title(f)

        fig.tight_layout()
        plt.savefig('fpopl_data6.png')
        return Response(status=200)

class CoronaDataAnalysis(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def corona_data_analysis(self, *args, **kwargs):
        f_path = "c:/Windows/Fonts/malgun.ttf"
        font_name = fm.FontProperties(fname=f_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)

        corona_data = CoronaData.objects.all()

        corona_df = pd.DataFrame(
            list(corona_data.values("serial_number", "date", "gugun")))

        corona_df['date'] = [''.join(x.split('-')[0:2])
                             for x in corona_df.date]  # 2020-01 2020-01 2021-03-07 -> 202001, 202103

        raw_1 = corona_df.groupby(
            by=['date', 'gugun']).count().reset_index()

        # 그래프 그리기
        raw_1 = raw_1.set_index('gugun')
        raw_1 = raw_1.drop('기타', axis=0)
        raw_1 = raw_1.drop('타시도', axis=0)

        raw_2 = raw_1
        raw_2 = raw_2.groupby(by=['date']).sum().reset_index()
        raw_2["serial_number"] = raw_2["serial_number"]/25

        fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(15, 15))

        for i, f in enumerate(raw_1.index.unique()):
            r = int(i / 5)  # 행별로 그래프 배치하기
            c = i % 5  # 열별로 그래프 배치하기

            df = raw_1[(raw_1.index == f)]

            line20 = sns.lineplot(
                data=raw_2, x='date', y='serial_number', label='average', ax=axes[r][c])
            line21 = sns.lineplot(
                data=df, x='date', y='serial_number', label='corona', ax=axes[r][c])

            line21.set_ylim(0, 800)
            line21.set_title(f)

        fig.tight_layout()
        plt.savefig('corona_data.png')
        return Response(status=200)