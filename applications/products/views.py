from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .decorators import acceptance_post_swagger, acceptance_get_swagger, acceptance_get_detail_swagger, \
    acceptance_delete_swagger, storage_post_swagger, storage_get_swagger, storage_delete_swagger, \
    storage_get_detail_swagger, wheel_post_swagger, wheel_delete_swagger, wheel_get_detail_swagger, wheel_put_swagger
from .models import Storage, Wheel, Acceptance
from .serializers import StorageSerializer, WheelSerializer, WheelListSerializer, AcceptanceSerializer, \
    AcceptanceListSerializer, AcceptanceDetailSerializer, WheelDetailSerializer
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class StorageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @storage_post_swagger
    def post(self, request, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_401_UNAUTHORIZED)
        context = {'request': request}
        serializer = StorageSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @storage_get_swagger
    def get(self, request, *args, **kwargs):
        storages = Storage.objects.filter(owner=request.user.team_id)
        serializer = StorageSerializer(storages, many=True)

        return Response(serializer.data)


class StorageDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @storage_delete_swagger
    def delete(self, request, storage_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        try:
            storage = Storage.objects.get(id=storage_id)
        except Storage.DoesNotExist:
            return Response({"msg": "Хранилище не найдено"}, status=status.HTTP_404_NOT_FOUND)
        storage.delete()
        return Response({'msg': "Хранилище успешно удалено"}, status=status.HTTP_204_NO_CONTENT)

    @storage_get_detail_swagger
    def get(self, request, storage_id, *args, **kwargs):
        search_query = request.query_params.get('search', '')
        season = request.query_params.get('season', '')
        if season:
            wheel_list = Wheel.objects.filter(Q(owner=request.user.team_id) & Q(storage=storage_id) &
                                              Q(title__icontains=search_query) & Q(season=season))
            serializer = WheelListSerializer(wheel_list, many=True)
        else:
            wheel_list = Wheel.objects.filter(Q(owner=request.user.team_id) & Q(storage=storage_id) &
                                              Q(title__icontains=search_query))
            serializer = WheelListSerializer(wheel_list, many=True)
        return Response(serializer.data)


class WheelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @wheel_post_swagger
    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = WheelSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class WheelDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @wheel_delete_swagger
    def delete(self, request, wheel_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        try:
            wheel = Wheel.objects.get(id=wheel_id)
        except Storage.DoesNotExist:
            return Response({"msg": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        wheel.delete()
        return Response({"msg": "Объект успешно удален"}, status=status.HTTP_204_NO_CONTENT)

    @wheel_get_detail_swagger
    def get(self, request, wheel_id, *args, **kwargs):
        try:
            wheel = Wheel.objects.get(id=wheel_id)
            serializer = WheelDetailSerializer(wheel, many=False)
            return Response(serializer.data)
        except Wheel.DoesNotExist:
            return Response({"msg": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)

    @wheel_put_swagger
    def put(self, request, wheel_id, *args, **kwargs):
        try:
            wheel = Wheel.objects.get(id=wheel_id, owner=request.user.team_id)
        except Wheel.DoesNotExist:
            return Response({"msg": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WheelSerializer(wheel, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AcceptanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @acceptance_post_swagger
    def post(self, request, *args, **kwargs):
        print(request.user.functions)
        if not request.user.functions.get('Создание приемки', False):
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        context = {'request': request}
        serializer = AcceptanceSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Ваша приемка успешно добавлена"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @acceptance_get_swagger
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        storage_id = request.query_params.get('storage_id')
        season = request.query_params.get('season')
        filters = {'owner': request.user.team_id}
        if start_date:
            filters['created_at__gte'] = start_date
        if end_date:
            filters['created_at__lte'] = end_date
        if storage_id:
            filters['storage_id'] = storage_id
        if season:
            filters['season'] = season
        acceptance = Acceptance.objects.filter(**filters).order_by('-created_at')
        serializer = AcceptanceListSerializer(acceptance, many=True)
        return Response(serializer.data)


class AcceptanceDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @acceptance_get_detail_swagger
    def get(self, request, acceptance_id, *args, **kwargs):
        try:
            acceptance = Acceptance.objects.get(id=acceptance_id)
            serializer = AcceptanceDetailSerializer(acceptance, many=False)
            return Response(serializer.data)
        except Acceptance.DoesNotExist:
            return Response({"msg": 'Объект не найден'}, status=status.HTTP_400_BAD_REQUEST)

    @acceptance_delete_swagger
    def delete(self, request, acceptance_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        try:
            acceptance = Acceptance.objects.get(id=acceptance_id)
        except Acceptance.DoesNotExist:
            return Response({"msg": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        acceptance.delete()
        return Response({"msg": "Объект успешно удален"}, status=status.HTTP_204_NO_CONTENT)
