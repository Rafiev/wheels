from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
from applications.accounts import views


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('team/', views.GetTeamAPIView.as_view(), name='team'),
]