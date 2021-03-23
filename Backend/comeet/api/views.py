from rest_framework import status, viewsets, mixins 
from rest_framework.response import Response 
from django.views import View 
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from api.models import Code, Fpopl, Card, CoronaData
from .serializers import CodeSerializer, FpoplSerializer, CardSerializer, CoronaDataSerializer
from django.core.cache import cache
# Create your views here.

class CoronaSet(viewsets.GenericViewSet, mixins.ListModelMixin, View) :
    serializer_class = CoronaDataSerializer
                
    def get_queryset(self):
        corona_data = CoronaData.objects.all()
        if not corona_data.exists():
            raise  HttpResponse()
        # cd = CoronaDataSerializer(corona_data, many=True)
        print(corona_data)
        # 데이터를 하루동안 저장 
        # cache.set("corona_jongno", CoronaDataSerializer(corona_data.filter(gugun="종로구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_junggu", CoronaDataSerializer(corona_data.filter(gugun="종구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_yongsan", CoronaDataSerializer(corona_data.filter(gugun="용산구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_sd", CoronaDataSerializer(corona_data.filter(gugun="성동구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_gwangjin", CoronaDataSerializer(corona_data.filter(gugun="광진구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_ddm", CoronaDataSerializer(corona_data.filter(gugun="동대문구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_jungnang", CoronaDataSerializer(corona_data.filter(gugun="중랑구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_sb", CoronaDataSerializer(corona_data.filter(gugun="성북구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_gangbuk", CoronaDataSerializer(corona_data.filter(gugun="강북구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_dobong", CoronaDataSerializer(corona_data.filter(gugun="도봉구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_nowon", CoronaDataSerializer(corona_data.filter(gugun="노원구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_ep", CoronaDataSerializer(corona_data.filter(gugun="은평구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_sdm", CoronaDataSerializer(corona_data.filter(gugun="서대문구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_mapo", CoronaDataSerializer(corona_data.filter(gugun="마포구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_yangcheon", CoronaDataSerializer(corona_data.filter(gugun="양천구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_gangseo", CoronaDataSerializer(corona_data.filter(gugun="강서구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_guro", CoronaDataSerializer(corona_data.filter(gugun="구로구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_geumcheon", CoronaDataSerializer(corona_data.filter(gugun="금천구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_ydp", CoronaDataSerializer(corona_data.filter(gugun="영등포구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_dongjak", CoronaDataSerializer(corona_data.filter(gugun="동작구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_gwanak", CoronaDataSerializer(corona_data.filter(gugun="관악구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_seocho", CoronaDataSerializer(corona_data.filter(gugun="서초구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_gangnam", CoronaDataSerializer(corona_data.filter(gugun="강남구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_songpa", CoronaDataSerializer(corona_data.filter(gugun="송파구"), partial=True).data, 24 * 60 * 60)
        # cache.set("corona_gangdong", CoronaDataSerializer(corona_data.filter(gugun="강동구"), partial=True).data, 24 * 60 * 60)
        # return JsonResponse({'message' : 'CORONA_SUCCESS'},status=200)
        return corona_data[0]
class CodeSet(viewsets.GenericViewSet, mixins.ListModelMixin, View) :
    serializer_class = CodeSerializer
         
    def get_queryset(self):
        code_data = Code.objects.all()
        print()
        # 데이터를 하루동안 저장 
        cache.set("code_jongno", code_data.filter(signgu_nm="종로구"), 24 * 60 * 60)
        cache.set("code_junggu", code_data.filter(signgu_nm="종구"), 24 * 60 * 60)
        cache.set("code_yongsan", code_data.filter(signgu_nm="용산구"), 24 * 60 * 60)
        cache.set("code_sd", code_data.filter(signgu_nm="성동구"), 24 * 60 * 60)
        cache.set("code_gwangjin", code_data.filter(signgu_nm="광진구"), 24 * 60 * 60)
        cache.set("code_ddm", code_data.filter(signgu_nm="동대문구"), 24 * 60 * 60)
        cache.set("code_jungnang", code_data.filter(signgu_nm="중랑구"), 24 * 60 * 60)
        cache.set("code_sb", code_data.filter(signgu_nm="성북구"), 24 * 60 * 60)
        cache.set("code_gangbuk", code_data.filter(signgu_nm="강북구"), 24 * 60 * 60)
        cache.set("code_dobong", code_data.filter(signgu_nm="도봉구"), 24 * 60 * 60)
        cache.set("code_nowon", code_data.filter(signgu_nm="노원구"), 24 * 60 * 60)
        cache.set("code_ep", code_data.filter(signgu_nm="은평구"), 24 * 60 * 60)
        cache.set("code_sdm", code_data.filter(signgu_nm="서대문구"), 24 * 60 * 60)
        cache.set("code_mapo", code_data.filter(signgu_nm="마포구"), 24 * 60 * 60)
        cache.set("code_yangcheon", code_data.filter(signgu_nm="양천구"), 24 * 60 * 60)
        cache.set("code_gangseo", code_data.filter(signgu_nm="강서구"), 24 * 60 * 60)
        cache.set("code_guro", code_data.filter(signgu_nm="구로구"), 24 * 60 * 60)
        cache.set("code_geumcheon", code_data.filter(signgu_nm="금천구"), 24 * 60 * 60)
        cache.set("code_ydp", code_data.filter(signgu_nm="영등포구"), 24 * 60 * 60)
        cache.set("code_dongjak", code_data.filter(signgu_nm="동작구"), 24 * 60 * 60)
        cache.set("code_gwanak", code_data.filter(signgu_nm="관악구"), 24 * 60 * 60)
        cache.set("code_seocho", code_data.filter(signgu_nm="서초구"), 24 * 60 * 60)
        cache.set("code_gangnam", code_data.filter(signgu_nm="강남구"), 24 * 60 * 60)
        cache.set("code_songpa", code_data.filter(signgu_nm="송파구"), 24 * 60 * 60)
        cache.set("code_gangdong", code_data.filter(signgu_nm="강동구"), 24 * 60 * 60)

        return JsonResponse({'message' : 'CODE_SUCCESS'},status=200)
class FpoplSet(viewsets.GenericViewSet, mixins.ListModelMixin, View) :
    serializer_class = FpoplSerializer

    def get_queryset(self):
        fpopl_data = Fpopl.objects.all()
        # 데이터를 하루동안 저장 
        cache.set("fpopl_jongno", fpopl_data.filter(gugun="종로구"), 24 * 60 * 60)
        cache.set("fpopl_junggu", fpopl_data.filter(gugun="종구"), 24 * 60 * 60)
        cache.set("fpopl_yongsan", fpopl_data.filter(gugun="용산구"), 24 * 60 * 60)
        cache.set("fpopl_sd", fpopl_data.filter(gugun="성동구"), 24 * 60 * 60)
        cache.set("fpopl_gwangjin", fpopl_data.filter(gugun="광진구"), 24 * 60 * 60)
        cache.set("fpopl_ddm", fpopl_data.filter(gugun="동대문구"), 24 * 60 * 60)
        cache.set("fpopl_jungnang", fpopl_data.filter(gugun="중랑구"), 24 * 60 * 60)
        cache.set("fpopl_sb", fpopl_data.filter(gugun="성북구"), 24 * 60 * 60)
        cache.set("fpopl_gangbuk", fpopl_data.filter(gugun="강북구"), 24 * 60 * 60)
        cache.set("fpopl_dobong", fpopl_data.filter(gugun="도봉구"), 24 * 60 * 60)
        cache.set("fpopl_nowon", fpopl_data.filter(gugun="노원구"), 24 * 60 * 60)
        cache.set("fpopl_ep", fpopl_data.filter(gugun="은평구"), 24 * 60 * 60)
        cache.set("fpopl_sdm", fpopl_data.filter(gugun="서대문구"), 24 * 60 * 60)
        cache.set("fpopl_mapo", fpopl_data.filter(gugun="마포구"), 24 * 60 * 60)
        cache.set("fpopl_yangcheon", fpopl_data.filter(gugun="양천구"), 24 * 60 * 60)
        cache.set("fpopl_gangseo", fpopl_data.filter(gugun="강서구"), 24 * 60 * 60)
        cache.set("fpopl_guro", fpopl_data.filter(gugun="구로구"), 24 * 60 * 60)
        cache.set("fpopl_geumcheon", fpopl_data.filter(gugun="금천구"), 24 * 60 * 60)
        cache.set("fpopl_ydp", fpopl_data.filter(gugun="영등포구"), 24 * 60 * 60)
        cache.set("fpopl_dongjak", fpopl_data.filter(gugun="동작구"), 24 * 60 * 60)
        cache.set("fpopl_gwanak", fpopl_data.filter(gugun="관악구"), 24 * 60 * 60)
        cache.set("fpopl_seocho", fpopl_data.filter(gugun="서초구"), 24 * 60 * 60)
        cache.set("fpopl_gangnam", fpopl_data.filter(gugun="강남구"), 24 * 60 * 60)
        cache.set("fpopl_songpa", fpopl_data.filter(gugun="송파구"), 24 * 60 * 60)
        cache.set("fpopl_gangdong", fpopl_data.filter(gugun="강동구"), 24 * 60 * 60)

        return JsonResponse({'message' : 'FPOPL_SUCCESS'},status=200)

class CoronaList(viewsets.GenericViewSet, mixins.ListModelMixin, View) :
    serializer_class = CoronaDataSerializer

    def get_queryset(self): 
        jong = cache.get("code_jongno")
        return jong

# @api_view(['GET'])
# @swagger_auto_schema()
# def Code_list(request):
#     # GET list of api, POST a new api, DELETE all api
#     if request.method == 'GET':
#         api = Code.objects.filter(brtc_nm="서울특별시")

#         #title = request.GET.get('title', None)
#         # if title is not None:
#         #     addrs = addrs.filter(title__icontains=title)

#         api.serializers = CodeSerializer(api, many=True)

#         # 데이터를 하루동안 저장 
#         cache.set("corona", api.serializers.data, 24 * 60 * 60)
#         print(cache.get("corona"))

#         return JsonResponse(api.serializers.data, safe=False)


# @api_view(['GET'])
# def CoronaData_list(request):
#     # GET list of api, POST a new api, DELETE all api
#     if request.method == 'GET':
#         api = CoronaData.objects.filter(gugun="강서구", overseas="-")

#         #title = request.GET.get('title', None)
#         # if title is not None:
#         #     addrs = addrs.filter(title__icontains=title)

#         api.serializers = CoronaDataSerializer(api, many=True)

#         # 데이터를 하루동안 저장 
#         cache.set("corona", api.serializers.data, 24 * 60 * 60)
#         print(cache.get("corona"))

#         return JsonResponse(api.serializers.data, safe=False)


# @api_view(['GET'])
# def Fpopl_list(request):
#     # GET list of api, POST a new api, DELETE all api
#     if request.method == 'GET':
#         api = Fpopl.objects.filter(date="20210101", gugun="구로구")

#         #title = request.GET.get('title', None)
#         # if title is not None:
#         #     addrs = addrs.filter(title__icontains=title)

#         api.serializers = FpoplSerializer(api, many=True)
        
#         # 데이터를 하루동안 저장 
#         cache.set("fpopl", api.serializers.data, 24 * 60 * 60)
#         print(cache.get("fpopl"))
        
#         return JsonResponse(api.serializers.data, safe=False)

