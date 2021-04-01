from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from django.http.response import JsonResponse
from api.models import Code, Fpopl, Card, CoronaData, Gugun, Fpopl_BC
from user.models import SearchLog
from .serializers import CodeSerializer, FpoplSerializer, CardSerializer, CoronaDataSerializer, CodeBodySerializer
from user.serializers import SearchSerializer, SearchLogSerializer, SearchBodySerializer, SearchLogBodySerializer
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
import io
import urllib
import base64
from datetime import datetime, timedelta
from collections import Counter
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
        corona_queryset = CoronaData.objects.filter(date__contains="2021-02")
        # corona_queryset = cache.get("corona_data")

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
        # 주어지는 주소 기반으로 중간지점을 가져오는 로직
        mid = midpoint(request.data['signgu_nm'])
        # 중간 지점을 기반으로 가까운 지역 리스트 조회
        nlist = nearbyArea(mid)
        # 로케이션 : lat , lng
        temp_area = nlist[0]
        print(temp_area)
        recomm_loc = Gugun.objects.filter(signgu_nm=temp_area)
        for loc in recomm_loc.iterator():
            lat = loc.lat
            lng = loc.lng
        # 첫번째 딕셔너리 완성
        loc_data = {"recomm_lat": lat,
                    "recomm_lng": lng, "signgu_nm": temp_area}

        # 해당 구의 코로나 정보 뽑아오기(해당 구에 사망하였거나 아직 완치되지 않은 데이터 추출)
        target_corona_data = CoronaData.objects.filter(
            gugun=temp_area).exclude(discharge="퇴원")
        # 월별로 정렬
        df = pd.DataFrame(list(target_corona_data.values("gugun", "date")))
        # 먼저 일별로 정리
        df = df.groupby(by=["date"], as_index=False).count()
        # 월별로 통합
        # print(df["date"].str.contains("2021-03")["gugun"])
        df_2003 = df[df["date"].str.contains("2020-03")]
        df_2004 = df[df["date"].str.contains("2020-04")]
        df_2005 = df[df["date"].str.contains("2020-05")]
        df_2006 = df[df["date"].str.contains("2020-06")]
        df_2007 = df[df["date"].str.contains("2020-07")]
        df_2008 = df[df["date"].str.contains("2020-08")]
        df_2009 = df[df["date"].str.contains("2020-09")]
        df_2010 = df[df["date"].str.contains("2020-10")]
        df_2011 = df[df["date"].str.contains("2020-11")]
        df_2012 = df[df["date"].str.contains("2020-12")]
        df_2101 = df[df["date"].str.contains("2021-01")]
        df_2102 = df[df["date"].str.contains("2021-02")]
        df_2103 = df[df["date"].str.contains("2021-03")]

        corona_data = {'date': ["2020-03", "2020-04", "2020-05", "2020-06", "2020-07", "2020-08", "2020-09", "2020-10", "2020-11", "2020-12", "2021-01", "2021-02", "2021-03"],
                       'patients': [int(df_2003["gugun"].sum()), int(df_2004["gugun"].sum()), int(df_2005["gugun"].sum()), int(df_2006["gugun"].sum()),
                                    int(df_2007["gugun"].sum()), int(df_2008["gugun"].sum()), int(
                           df_2009["gugun"].sum()), int(df_2010["gugun"].sum()),
            int(df_2011["gugun"].sum()), int(df_2012["gugun"].sum()), int(df_2101["gugun"].sum()), int(df_2102["gugun"].sum()), int(df_2103["gugun"].sum())]}

        print(corona_data)
        print("===========================================")

        total_data = {**loc_data, **corona_data}

        data = cache.get("fpopl_data")

        # 해당 구의 유동인구 데이터
        target_fpopl_data = data.filter(
            gugun=temp_area).exclude(age_range=60).exclude(age_range=70).filter(per_time="21")
        target_fpopl_bc_data = Fpopl_BC.objects.filter(
            gugun=temp_area).exclude(age_range=60).exclude(age_range=70).filter(per_time="21")

        fpopl_df = pd.DataFrame(list(target_fpopl_data.values("date", "popl")))
        fpopl_df.loc[(fpopl_df['date'] >= "20200101") & (
            fpopl_df['date'] <= "20200131"), 'date'] = "202001"
        fpopl_df.loc[(fpopl_df['date'] >= "20200201") & (
            fpopl_df['date'] <= "20200229"), 'date'] = "202002"
        fpopl_df.loc[(fpopl_df['date'] >= "20200301") & (
            fpopl_df['date'] <= "20200331"), 'date'] = "202003"
        fpopl_df.loc[(fpopl_df['date'] >= "20200401") & (
            fpopl_df['date'] <= "20200430"), 'date'] = "202004"
        fpopl_df.loc[(fpopl_df['date'] >= "20200501") & (
            fpopl_df['date'] <= "20200531"), 'date'] = "202005"
        fpopl_df.loc[(fpopl_df['date'] >= "20200601") & (
            fpopl_df['date'] <= "20200630"), 'date'] = "202006"
        fpopl_df.loc[(fpopl_df['date'] >= "20200701") & (
            fpopl_df['date'] <= "20200731"), 'date'] = "202007"
        fpopl_df.loc[(fpopl_df['date'] >= "20200801") & (
            fpopl_df['date'] <= "20200831"), 'date'] = "202008"
        fpopl_df.loc[(fpopl_df['date'] >= "20200901") & (
            fpopl_df['date'] <= "20200930"), 'date'] = "202009"
        fpopl_df.loc[(fpopl_df['date'] >= "20201001") & (
            fpopl_df['date'] <= "20201031"), 'date'] = "202010"
        fpopl_df.loc[(fpopl_df['date'] >= "20201101") & (
            fpopl_df['date'] <= "20201130"), 'date'] = "202011"
        fpopl_df.loc[(fpopl_df['date'] >= "20201201") & (
            fpopl_df['date'] <= "20201231"), 'date'] = "202012"
        fpopl_df.loc[(fpopl_df['date'] >= "20210101") & (
            fpopl_df['date'] <= "20210131"), 'date'] = "202101"
        fpopl_df.loc[(fpopl_df['date'] >= "20210201") & (
            fpopl_df['date'] <= "20210228"), 'date'] = "202102"

        fpopl_df = fpopl_df.groupby("date").mean()
        fpopl_data = fpopl_df.to_dict('split')
        print(fpopl_df)
        total_data = {**total_data, **fpopl_data}

        # 코로나 이전 유동인구 데이터 확인
        fpopl_BC_df = pd.DataFrame(
            list(target_fpopl_bc_data.values("date", "popl")))
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190301") & (
            fpopl_BC_df['date'] <= "20190331"), 'date'] = "201903"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190401") & (
            fpopl_BC_df['date'] <= "20190430"), 'date'] = "201904"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190501") & (
            fpopl_BC_df['date'] <= "20190531"), 'date'] = "201905"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190601") & (
            fpopl_BC_df['date'] <= "20190630"), 'date'] = "201906"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190701") & (
            fpopl_BC_df['date'] <= "20190731"), 'date'] = "201907"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190801") & (
            fpopl_BC_df['date'] <= "20190831"), 'date'] = "201908"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20190901") & (
            fpopl_BC_df['date'] <= "20190930"), 'date'] = "201909"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20191001") & (
            fpopl_BC_df['date'] <= "20191031"), 'date'] = "201910"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20191101") & (
            fpopl_BC_df['date'] <= "20191130"), 'date'] = "201911"
        fpopl_BC_df.loc[(fpopl_BC_df['date'] >= "20191201") & (
            fpopl_BC_df['date'] <= "20191231"), 'date'] = "201912"

        fpopl_BC_df = fpopl_BC_df.groupby("date").mean()
        # fpopl_BC_data = fpopl_BC_df.to_dict('split')
        print("===========================================")
        print(fpopl_BC_df)
        return JsonResponse(total_data, safe=False)

# 거리 지수 저장
class SaveDistWeight(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    serializer_class = SearchLogSerializer

    @swagger_auto_schema(request_body=SearchLogBodySerializer)
    def save_recomm_list(self, request, *args, **kwargs):

        # 입력된 위치 기반 중간지점 도출 => 구로 변환
        mid = midpoint(request.data['searchList'])
        
        # 중간 지점을 기반으로 가까운 지역 순으로 리스트 조회
        nlist = nearbyArea(mid)

        # 현재는 인덱스 값으로 저장 => 거리 가중치로 변환해야됨 
        dist_weights = {string : 25 - i for i,string in enumerate(nlist)}
        # print(dist_weights)
        return Response(status=200)

def midpoint(loc):
    area = []

    target_lat = 0.0
    target_lng = 0.0

    for i in loc:
        target_lat += i["lat"]
        target_lng += i["lng"]

    target_lat /= len(loc)
    target_lng /= len(loc)

    get_list = Gugun.objects.all()

    for i in get_list.iterator():
        area.append([i.signgu_nm])

    cnt = 0

    for i in get_list.iterator():

        dist = (float(i.lat) - target_lat) * (float(i.lat) - target_lat) + (
            float(i.lng) - target_lng)*(float(i.lng) - target_lng)

        area[cnt].append(dist)

        cnt += 1

    area.sort(key=lambda x: x[1])

    print(area[0][0])

    return area[0][0]

def nearbyArea(loc):
    area = []

    target = Gugun.objects.filter(signgu_nm=loc)
    others = Gugun.objects.all()

    for i in target.iterator():
        target_lat = float(i.lat)
        target_lng = float(i.lng)

    for i in others.iterator():
        area.append([i.signgu_nm])

    cnt = 0

    for i in others.iterator():

        dist = (float(i.lat) - target_lat) * (float(i.lat) - target_lat) + (
            float(i.lng) - target_lng)*(float(i.lng) - target_lng)

        area[cnt].append(dist)

        cnt += 1

    area.sort(key=lambda x: x[1])

    area_list = []

    for i in area:
        area_list.append(i[0])

    return area_list

# 코로나 지수 저장
class SaveCoronaWeight(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    def save_corona_weight(self, *args, **kwargs):
        return None

# 유동인구 지수 저장
class SaveFpoplWeight(viewsets.GenericViewSet, mixins.ListModelMixin, View):
    def save_fpopl_weight(self, *args, **kwargs):
        today = datetime.today()

        cal = today - datetime(2020, 12, 1, 0, 0, 0)
        # print(cal.days)
        standard = today - timedelta(cal.days)
        fpopl_list = Fpopl.objects.filter(
            date__range=[standard.strftime('%Y%m%d'), today.strftime('%Y%m%d')]
        )
        df = pd.DataFrame(list(fpopl_list.values("date", "popl", "gugun")))

        df['date'] = [ x[0:6] for x in df.date]  # 2020-01 2020-01 2021-03-07 -> 202001, 202103
        # print(df)
        df = df.groupby(by=["gugun", "date"], as_index=False).sum()
        # print(df)

        # 월별 총 유동인구수 
        df_first = df[df['date'] == '202012'].groupby(by=['date']).sum()
        df_second = df[df['date'] == '202101'].groupby(by=['date']).sum()
        df_third = df[df['date'] == '202102'].groupby(by=['date']).sum()

        a = df_first.iloc[0]['popl']
        b = df_second.iloc[0]['popl']
        c = df_third.iloc[0]['popl']
        # print(a)
        # print(b)
        # print(c)

        # 상대적 유동인구 분포율 
        relative_first = df[df['date'] == '202012']
        relative_first['popl'] =[(x/a)*100 for x in relative_first.popl]
        relative_second = df[df['date'] == '202101']
        relative_second['popl'] = [(x/b)*100 for x in relative_second.popl]
        relative_third = df[df['date'] == '202102']
        relative_third['popl'] = [(x/c)*100 for x in relative_third.popl]
        
        # print(relative_first)
        # print(relative_second)
        # print(relative_third)

        # 유동인구수 평균 - 25개 구
        a = df_first.iloc[0]['popl'] / 25
        b = df_second.iloc[0]['popl'] / 25
        c = df_third.iloc[0]['popl'] / 25

        # 유동인구수 - 평균 유동인구수보다 유동인구수가 많은 지역을 1로 적은 지역은 0으로 표시
        absolute_first = df[df['date'] == '202012']
        absolute_first['popl'] =[1 if x - a > 0 else 0 for x in absolute_first.popl]
        absolute_second = df[df['date'] == '202101']
        absolute_second['popl'] = [1 if x - b > 0 else 0 for x in absolute_second.popl]
        absolute_third = df[df['date'] == '202102']
        absolute_third['popl'] = [ 1 if x - c > 0 else 0 for x in absolute_third.popl]

        # print(absolute_first)
        # print(absolute_second)
        # print(absolute_third)

        # 유동인구 변화량 계산 
        gugun_list = list(Gugun.objects.values())
        # print(gugun_list)
        data = {'gugun' : [], 'popl' : [], 'first_popl_rate' : [], 'second_popl_rate' : []}
        fpop_rate = pd.DataFrame(data)
        for i in range(0, len(gugun_list)):
            temp_df = df[df['gugun'] == gugun_list[i]['signgu_nm']]
            popl_first = temp_df.iloc[0]['popl']
            popl_second = temp_df.iloc[1]['popl']
            popl_third = temp_df.iloc[2]['popl']
            # 12~1월 유동인구 변화율
            temp_df['first_popl_rate'] = ((popl_second - popl_first) / popl_first) * 100
            # 1~2월 유동인구 변화율
            temp_df['second_popl_rate'] = ((popl_third - popl_second) / popl_second) * 100
            temp_df = temp_df.groupby(["gugun"], as_index=False).mean()
            # print(temp_df)
            fpop_rate = fpop_rate.append(temp_df, ignore_index=False)
        # print(fpop_rate.groupby(["gugun"], as_index=False).mean())
        
        # 해당 구의 유동인구 / 전체 유동인구 => 등수 뽑아 
        point_1 = relative_third.sort_values(by=['popl'], axis=0)
        list_1 = point_1['gugun'].to_list()
        weight_1 = {string : (i + 1) * 4 for i,string in enumerate(list_1)}
        # print(weight_1)
        # 첫번째 달에서 두번째 달 넘어가는 걸로 소트해서 등수 뽑아 (12 => 1)
        point_2 = fpop_rate.sort_values(by=['first_popl_rate'], axis=0)
        list_2 = point_2['gugun'].to_list()
        weight_2 = {string : (i + 1) * 1 for i,string in enumerate(list_2)}
        # print(weight_2)
        # 두번째 달 넘어가는 거에서 세번째 달 넘어가는 걸로 소트해서 등수 뽑아(1 => 2)
        point_3 = fpop_rate.sort_values(by=['second_popl_rate'], axis=0)
        list_3 = point_3['gugun'].to_list()
        weight_3 = {string : (i + 1) * 2 for i,string in enumerate(list_3)}
        # print(weight_3)

        total_score = Counter(weight_1) + Counter(weight_2) + Counter(weight_3)
        print(total_score)
        return Response(status=200)

class DataAnalysis(viewsets.GenericViewSet, mixins.ListModelMixin, View):

    def data_analysis(self, *args, **kwargs):
        f_path = "c:/Windows/Fonts/malgun.ttf"
        font_name = fm.FontProperties(fname=f_path).get_name()
        plt.rc('font', family=font_name)
        plt.rc('axes', unicode_minus=False)

        # bc_data = Fpopl_BC.objects.filter(
        #     per_time__in=["12", "18", "19", "20", "21", "22", "23"])
        # ac_data = Fpopl.objects.filter(
        #     per_time__in=["12", "18", "19", "20", "21", "22", "23"])
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
            # line21.set_ylim(0, 8e+06)
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

        # print(corona_df)

        corona_df['date'] = [''.join(x.split('-')[0:2])
                             for x in corona_df.date]  # 2020-01 2020-01 2021-03-07 -> 202001, 202103

        # print(corona_df)

        raw_1 = corona_df.groupby(
            by=['date', 'gugun']).count().reset_index()

        # raw_1["date"] = pd.to_datetime(raw_1["date"], format='%Y%m')

        # '연도', '월', '일' 컬럼 생성
        # raw_1['year'] = raw_1.date.dt.year
        # raw_1['month'] = raw_1.date.dt.month
        # raw_1['day'] = raw_1.date.dt.day
        # raw_1['year-month'] = raw_1['year'].apply(
        #    str) + '-' + raw_1['month'].apply(str)
        # print(raw_1)
        # raw_1 = raw_1.groupby(
        #     by=["gugun", "date"]).mean().reset_index()
        # raw_1 = temp.drop('day', axis=1)
        #raw_1 = temp.drop('month', axis=1)
        #raw_1 = temp.drop('year', axis=1)

        # 그래프 그리기
        raw_1 = raw_1.set_index('gugun')
        raw_1 = raw_1.drop('기타', axis=0)
        raw_1 = raw_1.drop('타시도', axis=0)

        raw_2 = raw_1
        raw_2 = raw_2.groupby(by=['date']).sum().reset_index()
        raw_2["serial_number"] = raw_2["serial_number"]/25

        # raw_1 = raw_1.groupby(
        #     by=["gugun", "date"]).mean().reset_index()

        fig, axes = plt.subplots(nrows=5, ncols=5, figsize=(15, 15))
        # print(raw_1.index.unique())
        # print(raw_1)

        for i, f in enumerate(raw_1.index.unique()):
            r = int(i / 5)  # 행별로 그래프 배치하기
            c = i % 5  # 열별로 그래프 배치하기

            # df20 = raw_1[(raw_1.index == f) & (raw_1.year == 2020)]
            # df21 = raw_1[(raw_1.index == f) & (raw_1.year == 2021)]
            df = raw_1[(raw_1.index == f)]

            #     data=df20, x='month', y='serial_number', label='2020', ax=axes[r][c])

            line20 = sns.lineplot(
                data=raw_2, x='date', y='serial_number', label='average', ax=axes[r][c])
            line21 = sns.lineplot(
                data=df, x='date', y='serial_number', label='corona', ax=axes[r][c])

            line21.set_ylim(0, 800)
            line21.set_title(f)

        fig.tight_layout()
        plt.savefig('corona_data.png')
        return Response(status=200)
