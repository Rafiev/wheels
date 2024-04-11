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
        instance.season = validated_data.get('season', instance.season)
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
    new_wheels = serializers.JSONField(read_only=True)

    class Meta:
        model = Acceptance
        fields = '__all__'

    def create(self, validated_data):
        new_wheels_data = self.initial_data.get('new_wheels', [])
        request = self.context.get('request')
        validated_data['owner'] = request.user.team
        validated_data['user'] = request.user
        wheels_data = validated_data.get('wheels', [])
        new_wheels_to_create = [Wheel(**wheel_data, owner=request.user.team, storage=validated_data['storage']) for
                                wheel_data in new_wheels_data]

        wheels_to_update = list()
        if wheels_data:
            for wheel_data in wheels_data:
                title = wheel_data['title']
                amount = wheel_data['amount']
                try:
                    wheel = Wheel.objects.get(owner=request.user.team, title=title, season=validated_data['season'],
                                              storage=validated_data['storage'])
                    wheel.amount += amount
                    wheels_to_update.append(wheel)
                except Wheel.DoesNotExist:
                    pass
            Wheel.objects.bulk_update(wheels_to_update, ['amount'])

        Wheel.objects.bulk_create(new_wheels_to_create)
        try:
            validated_data['wheels'].extend(new_wheels_data)
        except KeyError:
            validated_data['wheels'] = new_wheels_data
        for item in validated_data['wheels']:
            item['id'] = Wheel.objects.get(owner=request.user.team, title=item['title'], season=validated_data['season']).id
        acceptance = Acceptance.objects.create(**validated_data)
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
        fields = ['id', 'created_at', 'user', 'storage', ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['amount'] = 0
        for a in instance.wheels:
            representation['amount'] += a.get('amount', 0)
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

