from django.urls import path
from .views import StorageAPIView, WheelAPIView, AcceptanceAPIView, StorageDetailAPIView, WheelDetailAPIView, \
    AcceptanceDetailAPIView

urlpatterns = [
    path('storages/', StorageAPIView.as_view(), name='storage-list'),
    path('storages/<int:storage_id>/', StorageDetailAPIView.as_view(), name='storage-detail'),
    path('wheels/', WheelAPIView.as_view(), name='wheel-list'),
    path('wheels/<int:wheel_id>/', WheelDetailAPIView.as_view(), name='wheel-detail'),
    path('acceptance/', AcceptanceAPIView.as_view(), name='acceptance-list'),
    path('acceptance/<int:acceptance_id>/', AcceptanceDetailAPIView.as_view(), name='acceptance-detail'),
]