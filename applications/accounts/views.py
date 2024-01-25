from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.accounts.serializers import CustomUserSerializer, TeamSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Team

User = get_user_model()


class TeamAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    @staticmethod
    def get(request, *args, **kwargs):
        team = Team.objects.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetTeamAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):

        if not request.user.role == 'Owner':
            return Response({'msg': 'У вас нет прав на это'}, status=status.HTTP_401_UNAUTHORIZED)
        user_team = User.objects.filter(team_id=request.user.team_id)
        serializer = CustomUserSerializer(user_team, many=True)

        return Response(serializer.data)


class RegisterAPIView(views.APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.set_new_password()
            return Response({'msg': 'Пароль успешно обновлён'}, status=status.HTTP_200_OK)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):

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

        if serializer.is_valid():
            refresh = request.data.get('refresh')
            access_token = serializer.validated_data.get('access')
            data = {'access': access_token, 'refresh': refresh}
            return Response(data)

        return Response(serializer.errors, status=400)