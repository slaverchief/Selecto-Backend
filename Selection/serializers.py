from rest_framework import serializers
from .models import *





class SelectionSerializer(serializers.ModelSerializer):


    class Meta:
        model = Selection
        fields = '__all__'


class CharSerializer(serializers.ModelSerializer):

    class Meta:
        model = Char
        fields = '__all__'
