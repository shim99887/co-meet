from django.shortcuts import render
from django.http import HttpResponse


from api.serializers import ApiSerializer
from rest_framework.decorators import api_view
# Create your views here.


def index(request):
    return HttpResponse("Hello. Comeet")


@api_view(['GET', 'POST', 'DELETE'])
def Api_list(request):
    # GET list of api, POST a new api, DELETE all api
    return HttpResponse(status=200)
