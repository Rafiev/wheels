from rest_framework import views, status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.accounts.serializers import CustomUserSerializer, TeamSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Team
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.exceptions import APIException

User = get_user_model()

team_responses = {
    200: openapi.Response(description="Список команд", schema=TeamSerializer(many=True)),
    400: "Неверный запрос"
}

team_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'title': openapi.Schema(type=openapi.TYPE_STRING)},
    required=['title']
)

login_responses = {
    201: openapi.Response(description="Success",
                          schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                properties={'access': openapi.Schema(type=openapi.TYPE_STRING),
                                                            'refresh': openapi.Schema(type=openapi.TYPE_STRING)})),
    422: openapi.Response(description="Invalid login or password",
                          examples={'application/json': {'msg': 'Неправильный логин или пароль'}}),
    400: openapi.Response(description="Missing login or password",
                          examples={'application/json': {'msg': 'Введите логин и пароль'}})
}


class TeamAPIView(views.APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_summary="Получение списка команд",
        operation_description="Этот эндпоинт используется для получения списка всех команд.",
        responses=team_responses)
    def get(self, request, *args, **kwargs):
        team = Team.objects.all()
        serializer = TeamSerializer(team, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=team_request_body,
        operation_summary="Создание команды",
        operation_description="Этот эндпоинт используется для создания новой команды.",
        responses={201: openapi.Response(description="Команда успешно создана", schema=TeamSerializer),
                   400: "Неверный запрос"})
    def post(self, request, *args, **kwargs):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetTeamAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получение команды пользователя",
        operation_description="Этот эндпоинт используется для получения списка пользователей, принадлежащих к той же "
                              "команде, что и текущий пользователь. Только пользователи с ролью 'Owner' имеют доступ к "
                              "этому эндпоинту.",
        responses={
            200: openapi.Response(
                description="Список пользователей команды",
                schema=CustomUserSerializer,
                examples={'application/json': [{"email": "rafievvv@gmail.com", "role": "Owner", "team": 3},
                                               {"email": "islam@gmail.com", "role": "Worker", "team": 3},
                                               {"email": "a@a.com", "role": "Worker", "team": 3}]}),
            401: openapi.Response(
                description="Return when user dont have root",
                examples={'application/json': {'msg': 'У вас нет прав на это'}})}
    )
    def get(self, request, *args, **kwargs):

        if not request.user.role == 'Owner':
            return Response({'msg': 'У вас нет прав на это'}, status=status.HTTP_401_UNAUTHORIZED)
        user_team = User.objects.filter(team_id=request.user.team_id)
        serializer = CustomUserSerializer(user_team, many=True)

        return Response(serializer.data)


class RegisterAPIView(views.APIView):

    @swagger_auto_schema(
        request_body=CustomUserSerializer,
        responses={201: CustomUserSerializer, 400: 'Bad request'},
        operation_summary="Регистрация нового пользователя",
        operation_description="Создания нового пользователя в базу",
    )
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, min_length=6),
                'new_password_confirm': openapi.Schema(type=openapi.TYPE_STRING, min_length=6),},
                 required=['new_password', 'new_password_confirm']),
        responses={200: openapi.Response(description="Success",
                                         examples={'application/json': {'msg': 'Пароль успешно обновлён'}}),
                   400: 'Bad request'},
        operation_summary="Изменения пароля пользователя",)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.set_new_password()
            return Response({'msg': 'Пароль успешно обновлён'}, status=status.HTTP_200_OK)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses= login_responses,
        operation_summary="Логин",)
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

        if serializer.is_valid():
            refresh = request.data.get('refresh')
            access_token = serializer.validated_data.get('access')
            data = {'access': access_token, 'refresh': refresh}
            return Response(data)

        return Response(serializer.errors, status=400)