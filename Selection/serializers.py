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


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = '__all__'


class OptionCharSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionChar
        fields = '__all__'

class TGUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TGUser
        fields = '__all__'
