from rest_framework import serializers
from .models import *

class SelectionSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    def create(self, validated_data):
        obj = Selection.objects.create(**validated_data)
        return obj

    def update(self, instance, validated_data):
        print(validated_data)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
