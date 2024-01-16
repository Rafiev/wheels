from django.urls import path
from .views import StorageAPIView, WheelAPIView

urlpatterns = [
    path('storages/', StorageAPIView.as_view(), name='storage-list'),
    path('storages/<int:storage_id>/', StorageAPIView.as_view(), name='storage-detail'),
    path('wheels/', WheelAPIView.as_view(), name='wheel-list'),
    path('wheels/<int:wheel_id>/', WheelAPIView.as_view(), name='wheel-detail'),
]