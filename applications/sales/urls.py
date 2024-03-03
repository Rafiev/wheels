from django.urls import path

from applications.sales.views import SaleAPIView, ReturnAPIView, DefectAPIView, ActionAPIView, ActionDetailAPIView

urlpatterns = [
    path('sales/', SaleAPIView.as_view(), name='sale'),
    path('return/', ReturnAPIView.as_view(), name='return'),
    path('defect/', DefectAPIView.as_view(), name='defect'),
    path('', ActionAPIView.as_view(), name='action'),
    path('<int:action_id>/', ActionDetailAPIView.as_view(), name='action-detail'),
]