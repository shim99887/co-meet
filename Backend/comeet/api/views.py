from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from api.models import Code
from api.serializers import CodeSerializer
# Create your views here.


def index(request):
    return HttpResponse("Hello. Comeet")


@api_view(['GET', 'POST', 'DELETE'])
def Api_list(request):
    # GET list of api, POST a new api, DELETE all api
    if request.method == 'GET':
        api = Code.objects.filter(brtc_nm="서울특별시")

        #title = request.GET.get('title', None)
        # if title is not None:
        #     addrs = addrs.filter(title__icontains=title)

        api.serializers = CodeSerializer(api, many=True)
        return JsonResponse(api.serializers.data, safe=False)
