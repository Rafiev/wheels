from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Action
from .serializers import SaleSerializer, ReturnSerializer, DefectSerializer, ActionListSerializer, \
    ActionDetailSerializer
from .decorators import action_delete_swagger, sale_post_swagger, defect_post_swagger, return_post_swagger, \
    action_get_swagger, action_get_detail_swagger


class SaleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @sale_post_swagger
    def post(self, request, *args, **kwargs):
        if not request.user.functions.get('Создание продаж', False):
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        context = {'request': request}
        serializer = SaleSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Ваша продажа успешно добавлена"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ReturnAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @return_post_swagger
    def post(self, request, *args, **kwargs):
        if not request.user.functions.get('Возврат', False):
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        context = {'request': request}
        serializer = ReturnSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Ваш возврат успешно добавлен"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class DefectAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @defect_post_swagger
    def post(self, request, *args, **kwargs):
        if not request.user.functions.get('Брак', False):
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        context = {'request': request}
        serializer = DefectSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Ваш брак успешно добавлен"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ActionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @action_get_swagger
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        storage_id = request.query_params.get('storage_id')
        season = request.query_params.get('season')
        action_type = request.query_params.get('action_type')
        filters = {'owner': request.user.team_id}
        if start_date:
            filters['created_at__gte'] = start_date
        if end_date:
            filters['created_at__lte'] = end_date
        if storage_id:
            filters['storage_id'] = storage_id
        if season:
            filters['season'] = season
        if action_type:
            filters['action_type'] = action_type
        acceptance = Action.objects.filter(**filters).order_by('-created_at')
        serializer = ActionListSerializer(acceptance, many=True)
        return Response(serializer.data)


class ActionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @action_get_detail_swagger
    def get(self, request, action_id, *args, **kwargs):
        try:
            action = Action.objects.get(id=action_id)
            serializer = ActionDetailSerializer(action, many=False)
            return Response(serializer.data)
        except Action.DoesNotExist:
            return Response({"msg": 'Объект не найден'}, status=status.HTTP_400_BAD_REQUEST)

    @action_delete_swagger
    def delete(self, request, action_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        try:
            action = Action.objects.get(id=action_id)
        except Action.DoesNotExist:
            return Response({"msg": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        action.delete()
        return Response({"msg": "Объект успешно удален"}, status=status.HTTP_204_NO_CONTENT)
