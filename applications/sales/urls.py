from django.urls import path

from applications.sales.views import SaleAPIView, SaleDetailAPIView

urlpatterns = [
    path('sales/', SaleAPIView.as_view(), name='sales'),
    path('sales/<int:sale_id>/', SaleDetailAPIView.as_view(), name='sales-detail'),
]