from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .permissions import IsCorrectToken
from .calc import Matrix
from .decorators import catch_exceptions


class BaseSelectoApiView(APIView):
    permission_classes = (IsCorrectToken, )
    Serializer = None
    Model = None

    @catch_exceptions
    def get(self, request):
        serializers = self.Serializer(self.Model.objects.filter(**request.data), many=True)
        return Response({'result': serializers.data, 'status': 0})

    @catch_exceptions
    def post(self, request):
        serializer = self.Serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()
        return Response({'status': 0, 'result': obj.id})

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
            serializer.is_valid()
            serializer.save()
        return Response({'status': 0})

    @catch_exceptions
    def delete(self, request):
        self.Model.objects.get(**request.data).delete()
        return Response({'status': 0})


class SelectionView(BaseSelectoApiView):
    Serializer = SelectionSerializer
    Model = Selection


class CharView(BaseSelectoApiView):
    Serializer = CharSerializer
    Model = Char


class OptionView(BaseSelectoApiView):
    Serializer = OptionSerializer
    Model = Option


class OptionCharView(BaseSelectoApiView):
    Serializer = OptionCharSerializer
    Model = OptionChar

    @catch_exceptions
    def get(self, request):
        serializers = None
        if request.data.get('selection', None):
            objects = None
            chars = Char.objects.filter(selection=request.data.get('selection'))
            optionchars = self.Model.objects.filter(char__in=chars)
            serializers = self.Serializer(optionchars, many=True)
        else:
            serializers = self.Serializer(self.Model.objects.filter(**request.data), many=True)
        for data in serializers.data:
            for key in list(data.keys()):
                if key == 'char':
                    c = Char.objects.get(pk=data[key])
                    data[key] = c.name
                elif key == 'option':
                    o = Option.objects.get(pk=data[key])
                    data[key] = o.name
        return Response({'result': serializers.data, 'status': 0})

    def post(self, request):
        rd = request.data
        if OptionChar.objects.filter(char=rd.get('char'), option=rd.get('option')):
            request.data['select_char'] = rd.get('char')
            request.data['select_option'] = rd.get('option')
            del request.data['char'], request.data['option']
            return super().put(request)
        else:
            return super().post(request)


class TGUserAPIView(BaseSelectoApiView):
    Serializer = TGUserSerializer
    Model = TGUser

    @catch_exceptions
    def get(self, request):
        serializers = self.Serializer(self.Model.objects.get(**request.data))
        return Response({'result': serializers.data, 'status': 0})


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
        options = s.option_set.all()
        weight_each_char_matrix = Matrix(len(options), 0)
        for ci in range(len(chars)):
            c = chars[ci]
            char_option_matrix = Matrix(len(options), len(options))
            for i in range(len(options)):
                for j in range(len(options)):
                    oc1 = OptionChar.objects.filter(char=c, option=options[i])
                    oc2 = OptionChar.objects.filter(char=c, option=options[j])
                    if not oc1 or not oc2:
                        return Response({'status': 1, 'result': 'Допущена ошибка в заполнении выборки.'})
                    oc1, oc2 = oc1.first().value, oc2.first().value
                    char_option_matrix[i][j] = round(oc1/oc2, 3)

            weight_each_char_matrix.vert_unit_conc(Matrix.build_weight_table(char_option_matrix.normalise()))
        result_matrix = weight_each_char_matrix*Matrix.build_weight_table(pair_comp_matrix.normalise())
        maxi = result_matrix.vals.index(max(result_matrix.vals))
        return Response({'result': options[maxi].name, 'status': 0})



# Create your views here.
