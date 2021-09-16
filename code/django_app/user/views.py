from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import authenticate
from django.db import transaction
from django.http import HttpResponse, Http404
from rest_framework import authentication, permissions, generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.views import APIView
from .serializers import UserSerializer, UserLoginSerializer
from .models import MyUser

import json


# Create your views here.
class UserAuthenticationView(APIView):
    '''
    User001の実装
    '''
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    def options(self, request, id):
        response = HttpResponse()
        response['allow'] = ','.join(['post'])
        return response

    def post(self, request):
        json_data = json.loads(request.body)
        username = json_data['username']
        password = json_data['password']

        if MyUser.objects.filter(name=username).exists():
            return Response({'message': f'username {username} is already exist. please login.'}, status=status.HTTP_200_OK)

        # serializer = User(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_user = MyUser()
        new_user.name = username
        new_user.password = password
        new_user.save()
        return Response(status.HTTP_201_CREATED)


class UserLoginView(APIView):
    '''
    User002の実装
    '''
    # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        print(request.data)
        if "username" not in request.data.keys():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)
        if "password" not in request.data.keys():
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

        username = request.data["username"]
        pw = request.data["password"]

        user = MyUser.objects.filter(name=username, password=pw)

        if user.exists():
            value = user.values()[0]
            res = {
                "id": value['id'],
                "username": value['name']
            }

            return Response(res, status=status.HTTP_200_OK)

        else:
            res = {
                "id": None,
                "username": None
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
