from django.contrib.auth import login
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.models import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerPermission
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class SelectionView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerPermission)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        serializers = SelectionSerializer(Selection.objects.filter(**request.data), many=True)
        return Response({'result': serializers.data})

    def post(self, request):
        serializer = SelectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(owner=request.user)
        return Response({'status': 'success'})

    def put(self, request):
        try:
            select_dict = {}
            for key in request.data.keys():
                try:
                    flag, attribute = key.split('_')
                except ValueError:
                    continue
                if flag == 'select':
                    select_dict[attribute] = request.data.get(key)
            objs = Selection.objects.filter(**select_dict)
            for obj in objs:
                serializer = SelectionSerializer(instance=obj, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        except ObjectDoesNotExist:
            return Response({'status': f'Object with name {request.get('old_name')} doesnt exist'})
        return Response({'status': 'success'})

    def delete(self, request):
        try:
            Selection.objects.get(**request.data).delete()
        except ObjectDoesNotExist:
            return Response({'status': f'Object with name {request.data.get('name')} doesnt exist'})
        return Response({'status': 'success'})

# Create your views here.
