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
from .permissions import IsOwnerPermission, IsCorrectToken
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from django.db.utils import IntegrityError
from django.db.models import ObjectDoesNotExist
from .calc import Matrix




class BaseSelectoApiView(APIView):
    permission_classes = (IsCorrectToken, )
    Serializer = None
    Model = None

    def get(self, request):
        serializers = self.Serializer(self.Model.objects.filter(**request.data), many=True)
        return Response({'result': serializers.data})

    def post(self, request):
        try:
            serializer = self.Serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save()
            return Response({'status': 'success'})
        except IntegrityError:
            return Response({'status': "Some constraint is violated"})

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
            objs = self.Model.objects.filter(**select_dict)
            for obj in objs:
                given_data = request.data
                for key in obj.__dict__.keys():
                    if key not in given_data.keys():
                        given_data[key] = obj.__dict__[key]
                serializer = self.Serializer(instance=obj, data=given_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            return Response({'status': 'success'})
        except ObjectDoesNotExist:
            return Response({'status': f'Object doesnt exist'})
        except IntegrityError:
            return Response({'status': "Some constraint is violated"})

    def delete(self, request):
        try:
            self.Model.objects.get(**request.data).delete()
            return Response({'status': 'success'})
        except ObjectDoesNotExist:
            return Response({'status': f'Objects with such attributes do not exist'})


class SelectionView(BaseSelectoApiView):
    Serializer = SelectionSerializer
    Model = Selection

    def post(self, request):
        try:
            serializer = self.Serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            obj = serializer.save(owner=request.user)
            return Response({'status': 'success'})
        except IntegrityError:
            return Response({'status': "Some constraint is violated"})


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
    def get(self, request):
        try:
            sel_id = request.data.get('selection_id', None)
            if not sel_id:
                raise Exception("No selection ID")
            s = Selection.object.get(pk=sel_id)
            print(s.char_set.all())
        except ObjectDoesNotExist:
            return Response({'status': 'Selection with such id was not found'})
        except Exception as exc:
            return Response({'status': str(exc)})



# Create your views here.
