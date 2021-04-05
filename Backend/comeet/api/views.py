from rest_framework import status, viewsets, mixins
from django.views import View
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from api.models import Fpopl, CoronaData, Gugun, Fpopl_BC
from .serializers import FpoplSerializer
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
from drf_yasg.utils import swagger_auto_schema

class CoronaSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
        코로나 데이터를 레디스에 저장하는 API

        ---
        # 내용
            - serial_number : 연번
            - patient_number : 환자번호
            - date : 날짜
            - gugun : 군, 구
            - overseas : 해외 이력
            - route : 감염 경로
            - discharge : 퇴원, 사망 여부
    """
    def set_corona(self, *args, **kwargs):
        # MongoDB에서 코로나 데이터 받기, queryset 형태로 데이터 반환 
        corona_data = CoronaData.objects.all()

        # 데이터가 존재하지 않을때 에러 처리
        if not corona_data.exists():
            raise HttpResponse()

        # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("corona_data", corona_data, 24 * 60 * 60)

        return JsonResponse({"message": "CORONA_SUCCESS"}, status=200)

class FpoplSet(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    """
        유동인구 데이터를 레디스에 저장하는 API

        ---
        # 내용
            - date : 날짜
            - per_time : 1시간 단위의 시간
            - age_range : 나이대
            - sex : 성별
            - city : 시
            - gugun : 군, 구
            - popl : 유동인구수
    """
    def set_fpopl(self, *args, **kwargs):
        # MongoDB에서 유동인구 데이터 받기, queryset 형태로 데이터 반환 
        fpopl_data = Fpopl.objects.all()

        # 데이터가 존재하지 않을때 에러 처리
        if not fpopl_data.exists():
            raise HttpResponse()

        # 데이터를 하루동안 저장, 자르기 편하게 queryset 형식으로
        cache.set("fpopl_data", fpopl_data, 24 * 60 * 60)

        return JsonResponse({'message': 'FPOPL_SUCCESS'}, status=200)

class CoronaList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    # 코로나 리스트 반환 
    """
        이전 달의 코로나 데이터를 전달하는 API

        ---
        # 내용
            - serial_number : 연번(해당 달의 총 감염자 수)
            - gugun : 군, 구
    """
    def get_corona_list(self, *args, **kwargs):
        # 한 달전의 데이터를 전달하기 위해 날짜 설정
        today = date.today()

        if today.month < 2:
            previous_yymm = str(today.year - 1) + "-" + str(today.month + 11)
        elif today.month > 1 and today.month < 11:
            previous_yymm = str(today.year) + "-0" + str(today.month - 1)
        else :
           previous_yymm = str(today.year) + "-" + str(today.month - 1)
        
        # 코로나 데이터를 DB에서 검색
        corona_queryset = CoronaData.objects.filter(date__contains=previous_yymm)

        # 구군마다 전체 분포표(확진자 수 카운트)
        df = pd.DataFrame(
            list(corona_queryset.all().values("serial_number", "gugun")))
        df = df.groupby(["gugun"], as_index=False).count()

        df = df.drop(index=[8, 26], axis=0)  # 기타, 타시도 삭제

        corona_json = df.to_dict() # Json 데이터로 전달하기 위해 dictionary로 변환

        return JsonResponse(corona_json, safe=False)
class FpoplList(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    # 유동인구 리스트 반환
    """
        2달 전의 유동인구 데이터를 반환하는 API (SKT 유동인구 데이터 기준)

        ---
        # 내용
            - date : 날짜
            - per_time : 1시간 단위의 시간
            - age_range : 나이대
            - sex : 성별
            - city : 시
            - gugun : 군, 구
            - popl : 유동인구수
    """
    def get_fpopl_list(self, *args, **kwargs):
        # 두 달전의 유동인구 데이터를 전달하기 위해 날짜 설정
        today = date.today()

        if today.month < 3:
            previous_yymm = str(today.year - 1) + str(today.month + 10)
        elif today.month > 2 and today.month < 12:
            previous_yymm = str(today.year) + "0" + str(today.month - 2)
        else :
            previous_yymm = str(today.year) + str(today.month - 2)
        # 유동인구 데이터를 DB에서 검색
        fpopl_queryset = Fpopl.objects.filter(date__contains=previous_yymm)

        # 구별, 날짜별 유동인구수 분포 DataFrame 생성
        df = pd.DataFrame(list(fpopl_queryset.all().values("date", "gugun", "popl")))
        
        # Json 데이터로 전달하기 위해 dictionary로 변환
        fpopl = df.to_dict()
        return JsonResponse(fpopl, safe=False)

class FpoplDataAnalysis(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    # 유동인구 데이터 분석 함수
    """
        유동인구 데이터 분석 함수

        ---
        # 내용
            - 전체 데이터 뽑아오기 - fpopl_data1 과 fpopl_data2
            - 주요 시간대 : 점심시간, 저녁시간 데이터 뽑아오기 - fpopl_data3 과 fpopl_data4 
            - 나이대 : 20 - 30대 데이터 뽑아오기 - fpopl_data5
            - 나이대 : 20대 - 40대 데이터 뽑아오기 - fpopl_data6 (현재 이 부분)
            - 분석 내용을 사진으로 저장
    """
    def fpopl_data_analysis(self, *args, **kwargs):
        # 그래프의 한글 깨짐 방지, 폰트 연결
        f_path = "c:/Windows/Fonts/malgun.ttf"
        font_name = fm.FontProperties(fname=f_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)
        
        # 코로나 이전 유동인구, 이후 유동인구 데이터 뽑아오기
        # 나이대 : 20대 - 40대 데이터 뽑아오기 - fpopl_data6
        bc_data = Fpopl_BC.objects.filter(age_range__in=[20, 30, 40])
        ac_data = Fpopl.objects.filter(age_range__in=[20, 30, 40])

        # 전체 데이터 뽑아오기 - fpopl_data1 과 fpopl_data2
        # bc_data = Fpopl_BC.objects.all()
        # ac_data = Fpopl.objects.all()

        # 주요 시간대 : 점심시간, 저녁시간 데이터 뽑아오기 - fpopl_data3 과 fpopl_data4 
        # bc_data = Fpopl_BC.objects.filter(per_time__in=["12", "18", "19", "20", "21", "22", "23"])
        # ac_data = Fpopl.objects.filter(per_time__in=["12", "18", "19", "20", "21", "22", "23"])

        # 나이대 : 20 - 30대 데이터 뽑아오기 - fpopl_data5
        # bc_data = Fpopl_BC.objects.filter(age_range__in=[20, 30])
        # ac_data = Fpopl.objects.filter(age_range__in=[20, 30])

        # 비교를 위해 DataFrame으로 변환 
        bc_df = pd.DataFrame(list(bc_data.values("date", "gugun", "popl")))
        ac_df = pd.DataFrame(list(ac_data.values("date", "gugun", "popl")))
        # 전체 데이터를 한 곳에서 볼 수 있도록 합침
        total_df = pd.concat([bc_df, ac_df], axis=0, ignore_index=True)
        # 하루의 유동인구로 표를 합침
        raw_1 = total_df.groupby(by=['date', 'gugun']).sum().reset_index()
        # 월별 유동인구 표시를 위해 date 형식으로 변환 
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
    """
        코로나 데이터 분석 함수

        ---
        # 내용
            - 
    """
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