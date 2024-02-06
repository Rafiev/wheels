from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.accounts.serializers import CustomUserSerializer, TeamSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .decorators import change_password_swagger, register_swagger, login_swagger, get_users_swagger, team_post_swagger, \
    team_get_swagger
from .models import Team
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import APIException

User = get_user_model()


class TeamAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    @team_get_swagger
    def get(self, request, *args, **kwargs):
        team = Team.objects.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    @team_post_swagger
    def post(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetTeamAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @get_users_swagger
    def get(self, request, *args, **kwargs):

        if not request.user.role == 'Owner':
            return Response({'msg': 'У вас нет прав на это'}, status=status.HTTP_401_UNAUTHORIZED)
        user_team = User.objects.filter(team_id=request.user.team_id)
        serializer = CustomUserSerializer(user_team, many=True)

        return Response(serializer.data)


class RegisterAPIView(views.APIView):

    @register_swagger
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @change_password_swagger
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.set_new_password()
            return Response({'msg': 'Пароль успешно обновлён'}, status=status.HTTP_200_OK)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):

    @login_swagger
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except APIException as exc:
            response = self.handle_exception(exc)
            return response

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        if response.status_code == 401:
            response.status_code = 422
            response.data = {'msg': 'Неправильный логин или пароль'}

        if response.status_code == 400:
            errors = list(response.data.keys())
            if len(errors) == 2:
                response.data = {'msg': 'Введите логин и пароль'}
            else:
                field = 'пароль' if 'password' in errors else 'логин'
                response.data = {'msg': f'Введите {field}'}

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            if serializer.is_valid():
                refresh = request.data.get('refresh')
                access_token = serializer.validated_data.get('access')
                data = {'access': access_token, 'refresh': refresh}
                return Response(data)

            return Response(serializer.errors, status=400)
        except Exception as ex:
            return Response({"msg": "у вас истек токен"}, status=status.HTTP_401_UNAUTHORIZED)