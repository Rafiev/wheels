from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from applications.sales.serializers import SaleSerializer


class SaleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = SaleSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Ваша продажа успешно добавлена"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
