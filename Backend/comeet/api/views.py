from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from api.models import Code, Fpopl, Card, CoronaData
from api.serializers import CodeSerializer, FpoplSerializer, CardSerializer, CoronaDataSerializer

from django.core.cache import cache
# Create your views here.


def index(request):
    return HttpResponse("Hello. Comeet")


@api_view(['GET'])
def Code_list(request):
    # GET list of api, POST a new api, DELETE all api
    if request.method == 'GET':
        api = Code.objects.filter(brtc_nm="서울특별시")

        #title = request.GET.get('title', None)
        # if title is not None:
        #     addrs = addrs.filter(title__icontains=title)

        api.serializers = CodeSerializer(api, many=True)

        # 데이터를 하루동안 저장 
        cache.set("corona", api.serializers.data, 24 * 60 * 60)
        print(cache.get("corona"))

        return JsonResponse(api.serializers.data, safe=False)


@api_view(['GET'])
def CoronaData_list(request):
    # GET list of api, POST a new api, DELETE all api
    if request.method == 'GET':
        api = CoronaData.objects.filter(gugun="강서구", overseas="-")

        #title = request.GET.get('title', None)
        # if title is not None:
        #     addrs = addrs.filter(title__icontains=title)

        api.serializers = CoronaDataSerializer(api, many=True)

        # 데이터를 하루동안 저장 
        cache.set("corona", api.serializers.data, 24 * 60 * 60)
        print(cache.get("corona"))

        return JsonResponse(api.serializers.data, safe=False)


@api_view(['GET'])
def Fpopl_list(request):
    # GET list of api, POST a new api, DELETE all api
    if request.method == 'GET':
        api = Fpopl.objects.filter(date="20210101", gugun="구로구")

        #title = request.GET.get('title', None)
        # if title is not None:
        #     addrs = addrs.filter(title__icontains=title)

        api.serializers = FpoplSerializer(api, many=True)
        
        # 데이터를 하루동안 저장 
        cache.set("fpopl", api.serializers.data, 24 * 60 * 60)
        print(cache.get("fpopl"))
        
        return JsonResponse(api.serializers.data, safe=False)