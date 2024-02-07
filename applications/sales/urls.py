from django.urls import path

from applications.sales.views import SaleAPIView

urlpatterns = [
    path('sales/', SaleAPIView.as_view(), name='sales')
]