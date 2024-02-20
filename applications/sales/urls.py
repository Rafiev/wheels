from django.urls import path

from applications.sales.views import SaleAPIView, SaleDetailAPIView, DefectAPIView, DefectDetailAPIView, ReturnAPIView

urlpatterns = [
    path('sales/', SaleAPIView.as_view(), name='sales'),
    path('sales/<int:sale_id>/', SaleDetailAPIView.as_view(), name='sales-detail'),
    path('defect/', DefectAPIView.as_view(), name='defects'),
    path('defect/<int:def_id>/', DefectDetailAPIView.as_view(), name='defects-detail'),
    path('return/', ReturnAPIView.as_view(), name='return'),
]