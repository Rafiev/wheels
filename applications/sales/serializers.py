from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from applications.products.models import Wheel
from applications.products.serializers import StorageSerializer
from applications.sales.models import Sale


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user.team
        validated_data['user'] = request.user
        wheel_list = [i.values() for i in validated_data['wheels']]
        wheel_list_for_update = []
        for title, amount, price in wheel_list:
            try:
                wheel = Wheel.objects.get(owner=request.user.team, title=title, storage=validated_data['storage'])
            except Wheel.DoesNotExist:
                raise ValidationError({"msg": f'Данного продукта нет {title}'})
            if not wheel.amount >= amount:
                raise ValidationError({"msg": f'У вас недостаточно продукта {title} что бы продать его'})
            wheel.amount -= amount
            wheel_list_for_update.append(wheel)
        Wheel.objects.bulk_update(wheel_list_for_update, ['amount'])
        for item in validated_data['wheels']:
            item['total-cost'] = item['amount'] * item['price']
        sale = Sale.objects.create(**validated_data)
        return sale


class SaleListSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Sale
        fields = ['id', 'created_at', 'user', 'storage']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['amount'] = 0
        representation['total-cost'] = 0
        for a in instance.wheels:
            representation['amount'] += a.get('amount', 0)
            representation['total-cost'] += a.get('amount', 0) * a.get('price', 0)
        return representation


class SaleDetailSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Sale
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        representation['user'] = instance.user.email

        return representation

