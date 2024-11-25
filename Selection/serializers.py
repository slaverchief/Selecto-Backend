from rest_framework import serializers
from .models import *

class BaseSelectoSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.non_edit = ['id']
        super().__init__(*args, **kwargs)

    def update(self, instance, validated_data):
        for key in self.non_edit:
            try:
                del validated_data[key]
            except KeyError:
                pass
        return super().update(instance, validated_data)

class SelectionSerializer(BaseSelectoSerializer):
    def create(self, validated_data):
        self.non_edit += ['owner']
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'


class CharSerializer(BaseSelectoSerializer):
    def create(self, validated_data):
        self.non_edit += ['selection', '']
        return super().create(validated_data)

    class Meta:
        model = Char
        fields = '__all__'


class OptionSerializer(BaseSelectoSerializer):
    def create(self, validated_data):
        self.non_edit += ['selection']
        return super().create(validated_data)

    class Meta:
        model = Option
        fields = '__all__'


class OptionCharSerializer(BaseSelectoSerializer):
    def create(self, validated_data):
        self.non_edit += ['owner']
        return super().create(validated_data)

    class Meta:
        model = OptionChar
        fields = '__all__'

class UserSerializer(BaseSelectoSerializer):
    def create(self, validated_data):
        self.non_edit += ['auth_id']
        return super().create(validated_data)

    class Meta:
        model = User
        fields = '__all__'
