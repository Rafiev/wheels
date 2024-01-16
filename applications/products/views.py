from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Storage, Wheel
from .serializers import StorageSerializer, WheelSerializer, WheelListSerializer
from rest_framework.permissions import IsAuthenticated


class StorageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        context = {'request': request}
        serializer = StorageSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, storage_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "You do not have the right to do this"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            storage = Storage.objects.get(id=storage_id)
        except Storage.DoesNotExist:
            return Response({"msg": "Storage not found"}, status=status.HTTP_404_NOT_FOUND)
        storage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        if 'storage_id' in kwargs:
            return self.get_detail_storage(request, **kwargs)
        else:
            return self.get_list(request, **kwargs)

    @staticmethod
    def get_detail_storage(request, storage_id, *args, **kwargs):
        wheel_list = Wheel.objects.filter(owner=request.user.team_id, storage=storage_id)
        serializer = WheelListSerializer(wheel_list, many=True)

        return Response(serializer.data)

    @staticmethod
    def get_list(request, *args, **kwargs):
        storages = Storage.objects.filter(owner=request.user.team_id)
        serializer = StorageSerializer(storages, many=True)

        return Response(serializer.data)


class WheelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        context = {'request': request}
        serializer = WheelSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, wheel_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "You do not have the right to do this"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            wheel = Wheel.objects.get(id=wheel_id)
        except Storage.DoesNotExist:
            return Response({"msg": "Wheel not found"}, status=status.HTTP_404_NOT_FOUND)
        wheel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def get(request, wheel_id, *args, **kwargs):
        wheel = Wheel.objects.get(id=wheel_id)
        serializer = WheelSerializer(wheel, many=False)

        return Response(serializer.data)

    @staticmethod
    def put(request, wheel_id, *args, **kwargs):
        try:
            wheel = Wheel.objects.get(id=wheel_id, owner=request.user.team_id)
        except Wheel.DoesNotExist:
            return Response({"msg": "Wheel not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = WheelSerializer(wheel, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)