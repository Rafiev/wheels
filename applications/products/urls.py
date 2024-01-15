from django.urls import path
from .views import StorageAPIView

urlpatterns = [
    path('storages/', StorageAPIView.as_view(), name='storage-list'),
    path('storages/<int:storage_id>/', StorageAPIView.as_view(), name='storage-detail'),
]