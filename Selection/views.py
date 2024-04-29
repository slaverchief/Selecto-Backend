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
from .permissions import IsCorrectToken
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from django.db.models import ObjectDoesNotExist
from .calc import Matrix
from .decorators import catch_exceptions






class BaseSelectoApiView(APIView):
    permission_classes = (IsCorrectToken, )
    Serializer = None
    Model = None

    @catch_exceptions
    def get(self, request):
        serializers = self.Serializer(self.Model.objects.filter(**request.data), many=True)
        return Response({'result': serializers.data})

    @catch_exceptions
    def post(self, request):
        serializer = self.Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'status': 'success'})

    @catch_exceptions
    def put(self, request):
        select_dict = {}
        for key in request.data.keys():
            try:
                flag, attribute = key.split('_')
            except ValueError:
                continue
            if flag == 'select':
                select_dict[attribute] = request.data.get(key)
        objs = self.Model.objects.filter(**select_dict)
        for obj in objs:
            given_data = request.data
            for key in obj.__dict__.keys():
                if key not in given_data.keys():
                    given_data[key.replace('_id', '')] = obj.__dict__[key]
            serializer = self.Serializer(instance=obj, data=given_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response({'status': 'success'})

    @catch_exceptions
    def delete(self, request):
        self.Model.objects.get(**request.data).delete()
        return Response({'status': 'success'})


class SelectionView(BaseSelectoApiView):
    Serializer = SelectionSerializer
    Model = Selection

    @catch_exceptions
    def post(self, request):
        serializer = self.Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save(owner=request.user)
        return Response({'status': 'success'})


class CharView(BaseSelectoApiView):
    Serializer = CharSerializer
    Model = Char


class OptionView(BaseSelectoApiView):
    Serializer = OptionSerializer
    Model = Option


class OptionCharView(BaseSelectoApiView):
    Serializer = OptionCharSerializer
    Model = OptionChar

class CalcView(APIView):
    permission_classes = [IsCorrectToken]

    @catch_exceptions
    def get(self, request):
        sel = request.data.get('selection', None)
        if not sel:
            raise Exception("No selection ID")
        s = Selection.objects.get(pk=sel)
        chars = s.char_set.all()
        pair_comp_matrix = Matrix(len(chars), len(chars))
        for i in range(len(chars)):
            for j in range(len(chars)):
                pair_comp_matrix[i][j] = round(chars[i].priority/chars[j].priority, 3)
        weight_each_char_matrix = Matrix(len(chars), 0)
        options_queue = map(lambda x: x.name,s.option_set.all())
        print(list(options_queue))
        return Response({'status': 'success'})



# Create your views here.
