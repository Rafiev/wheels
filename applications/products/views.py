from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Storage
from .serializers import StorageSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly


class StorageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = StorageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, storage_id, *args, **kwargs):
        if request.user.role == 'Worker':
            return Response({"msg": "You do not have the right to do this"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            storage = Storage.objects.get(id=storage_id)
        except Storage.DoesNotExist:
            return Response({"msg": "Storage not found"}, status=status.HTTP_404_NOT_FOUND)

        storage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)