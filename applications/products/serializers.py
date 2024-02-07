from rest_framework import serializers
from .models import Storage, Wheel, Acceptance


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
        wheels_count = sum([i.amount for i in instance.wheels.all()])
        representation['amount'] = wheels_count
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
        return representation


class WheelListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wheel
        fields = ['id', 'title', 'amount']


class WheelDetailSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Wheel
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        return representation


class AcceptanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Acceptance
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user.team
        validated_data['user'] = request.user
        acceptance = Acceptance.objects.create(**validated_data)
        wheel_list = [i.values() for i in validated_data['wheels']]
        for title, amount in wheel_list:
            wheel, created = Wheel.objects.get_or_create(owner=request.user.team, title=title,
                                                         storage=validated_data['storage'])
            wheel.amount += amount
            wheel.save()

        return acceptance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        representation['user'] = instance.user.email
        return representation


class AcceptanceListSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Acceptance
        fields = ['id', 'created_at', 'user', 'storage']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['amount'] = 0
        for a in instance.wheels:
            representation['amount'] += list(a.values())[1]
        return representation


class AcceptanceDetailSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Acceptance
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        representation['user'] = instance.user.email
        return representation

