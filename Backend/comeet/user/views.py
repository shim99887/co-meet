from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from user.models import User
from user.serializers import UserSerializer

# Create your views here.


@api_view(['GET'])
def User_list(request):
    # GET list of user, POST a new user, DELETE all user
    if request.method == 'GET':
        user = User.objects.all()

        #title = request.GET.get('title', None)
        # if title is not None:
        #     addrs = addrs.filter(title__icontains=title)

        user.serializers = UserSerializer(user, many=True)
        return JsonResponse(user.serializers.data, safe=False)


@api_view(['GET'])
def check_email(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(email=request.GET['email'])
        except Exception as e:
            user = None

        result = {
            'result': 'success',
            'data': "not exist" if user is None else "exist"
        }

        return JsonResponse(result)
