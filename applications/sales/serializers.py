from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from applications.products.models import Wheel
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
        acceptance = Sale.objects.create(**validated_data)
        return acceptance

