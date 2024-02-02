from django.urls import path
from .views import StorageAPIView, WheelAPIView, AcceptanceAPIView

urlpatterns = [
    path('storages/', StorageAPIView.as_view(), name='storage-list'),
    path('storages/<int:storage_id>/', StorageAPIView.as_view(), name='storage-detail'),
    path('wheels/', WheelAPIView.as_view(), name='wheel-list'),
    path('wheels/<int:wheel_id>/', WheelAPIView.as_view(), name='wheel-detail'),
    path('acceptance/', AcceptanceAPIView.as_view(), name='acceptance-list'),
    path('acceptance/<int:acceptance_id>/', AcceptanceAPIView.as_view(), name='acceptance-detail'),
]