from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from applications.products.models import Wheel
from applications.products.serializers import StorageSerializer
from applications.sales.models import Action


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user.team
        validated_data['user'] = request.user
        validated_data['action_type'] = 'Продажа'
        wheel_list = [i.values() for i in validated_data['wheels']]
        wheel_list_for_update = []
        for title, amount, price in wheel_list:
            try:
                wheel = Wheel.objects.get(owner=request.user.team, title=title, storage=validated_data['storage'],
                                          season=validated_data['season'])
            except Wheel.DoesNotExist:
                raise ValidationError({"msg": f'Данного продукта нет {title} {validated_data["season"]} в наличии'})
            if not wheel.amount >= amount:
                raise ValidationError({"msg": f'У вас недостаточно продукта {title} {validated_data["season"]} что бы продать его'})
            wheel.amount -= amount
            wheel_list_for_update.append(wheel)
        Wheel.objects.bulk_update(wheel_list_for_update, ['amount'])
        for item in validated_data['wheels']:
            item['total-cost'] = item['amount'] * item['price']
            item['id'] = Wheel.objects.get(owner=request.user.team, title=item['title'], season=validated_data['season']).id
        sale = Action.objects.create(**validated_data)
        return sale


# class SaleListSerializer(serializers.ModelSerializer):
#     storage = StorageSerializer()
#
#     class Meta:
#         model = Sale
#         fields = ['id', 'created_at', 'user', 'storage']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['user'] = instance.user.email
#         representation['amount'] = sum([i.get('amount', 0) for i in instance.wheels])
#         representation['total-cost'] = sum([i.get('total-cost', 0) for i in instance.wheels])
#         return representation
#
#
# class SaleDetailSerializer(serializers.ModelSerializer):
#     storage = StorageSerializer()
#
#     class Meta:
#         model = Sale
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['owner'] = instance.owner.title
#         representation['user'] = instance.user.email
#
#         return representation
#

class DefectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user.team
        validated_data['user'] = request.user
        validated_data['action_type'] = 'Брак'
        defect_obj = Action.objects.create(**validated_data)
        return defect_obj

#
# class DefectListSerializer(serializers.ModelSerializer):
#     storage = StorageSerializer()
#
#     class Meta:
#         model = Defect
#         fields = ['id', 'created_at', 'user', 'storage']
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['user'] = instance.user.email
#
#         return representation
#
#
# class DefectDetailSerializer(serializers.ModelSerializer):
#     storage = StorageSerializer()
#
#     class Meta:
#         model = Defect
#         fields = '__all__'
#
#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation['owner'] = instance.owner.title
#         representation['user'] = instance.user.email
#
#         return representation


class ReturnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Action
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user.team
        validated_data['user'] = request.user
        validated_data['action_type'] = 'Возврат'
        wheels_data = validated_data.get('wheels', [])
        wheels_to_update = list()
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
        ret_obj = Action.objects.create(**validated_data)
        return ret_obj


class ActionListSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Action
        fields = ['id', 'created_at', 'user', 'storage', 'action_type']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['amount'] = 0
        for wheel in instance.wheels:
            representation['amount'] += wheel.get('amount', 0)
        return representation


class ActionDetailSerializer(serializers.ModelSerializer):
    storage = StorageSerializer()

    class Meta:
        model = Action
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.title
        representation['user'] = instance.user.email
        return representation

