from django.urls import path
from applications.accounts import views


urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', views.CustomTokenRefreshView.as_view(), name='custom_token_refresh'),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('users_team/', views.GetTeamAPIView.as_view(), name='users_team'),
    path('team/', views.AdminTeamAPIView.as_view(), name='team'),
    path('change_password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('profile/', views.UserProfile.as_view(), name='profile'),
    path('user_off/', views.UserOffAPIView.as_view(), name='user-off')
]