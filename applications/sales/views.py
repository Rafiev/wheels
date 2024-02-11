from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from applications.sales.decorators import sale_post_swagger, sale_get_swagger, sale_get_detail_swagger, \
    sale_delete_swagger
from applications.sales.models import Sale
from applications.sales.serializers import SaleSerializer, SaleListSerializer, SaleDetailSerializer


class SaleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @sale_post_swagger
    def post(self, request, *args, **kwargs):
        context = {'request': request}
        serializer = SaleSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Ваша продажа успешно добавлена"}, status=status.HTTP_201_CREATED)
        return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @sale_get_swagger
    def get(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        storage_id = request.query_params.get('storage_id')
        filters = {'owner': request.user.team_id}
        if start_date:
            filters['created_at__gte'] = start_date
        if end_date:
            filters['created_at__lte'] = end_date
        if storage_id:
            filters['storage_id'] = storage_id
        sale = Sale.objects.filter(**filters)
        serializer = SaleListSerializer(sale, many=True)
        return Response(serializer.data)


class SaleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @sale_get_detail_swagger
    def get(self, request, sale_id, *args, **kwargs):
        try:
            sale = Sale.objects.get(id=sale_id)
            serializer = SaleDetailSerializer(sale, many=False)
            return Response(serializer.data)
        except Sale.DoesNotExist:
            return Response({"msg": 'Объект не найден'}, status=status.HTTP_400_BAD_REQUEST)

    @sale_delete_swagger
    def delete(self, request, sale_id, *args, **kwargs):
        if not request.user.role == 'Owner':
            return Response({"msg": "У вас нет прав на это"}, status=status.HTTP_409_CONFLICT)
        try:
            sale_obj = Sale.objects.get(id=sale_id)
        except Sale.DoesNotExist:
            return Response({"msg": "Объект не найден"}, status=status.HTTP_404_NOT_FOUND)
        sale_obj.delete()
        return Response({"msg": "Объект успешно удален"}, status=status.HTTP_204_NO_CONTENT)
