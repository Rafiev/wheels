from rest_framework import serializers
from .models import Storage, Wheel


class StorageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Storage
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        team_id = request.user.team_id
        validated_data['owner'] = request.user.team
        storage = Storage.objects.create(**validated_data)
        return storage

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        return representation


class WheelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wheel
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

    def create(self, validated_data):
        request = self.context.get('request')
        team_id = request.user.team_id
        validated_data['owner'] = request.user.team
        wheel = Wheel.objects.create(**validated_data)
        return wheel

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        representation['storage'] = instance.storage.title
        return representation


class WheelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wheel
        fields = ['id', 'title']