from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from applications.accounts.serializers import CustomUserSerializer, TeamSerializer

team_responses = {
    200: openapi.Response(description="Список команд", schema=TeamSerializer(many=True))
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
                          examples={'application/json': {'msg': 'Введите логин и пароль'}})}

register_swagger = swagger_auto_schema(
    request_body=CustomUserSerializer,
    responses={201: CustomUserSerializer, 400: openapi.Response(
        description="",  examples={'application/json': {'msg': 'serializers.errors'}})},
    operation_summary="Регистрация нового пользователя",
    operation_description="Создания нового пользователя в базу",)


change_password_swagger = swagger_auto_schema(
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'new_password': openapi.Schema(type=openapi.TYPE_STRING, min_length=6),
        'new_password_confirm': openapi.Schema(type=openapi.TYPE_STRING, min_length=6), },
                                  required=['new_password', 'new_password_confirm']),
    responses={200: openapi.Response(description="", examples={'application/json': {'msg': 'Пароль успешно обновлён'}}),
               400: openapi.Response(description="", examples={'application/json': {'msg': 'serializers.errors'}})},
    operation_summary="Изменения пароля пользователя",
)

login_swagger = swagger_auto_schema(
        responses=login_responses,
        operation_summary="Логин",)


get_users_swagger = swagger_auto_schema(
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

team_get_swagger = swagger_auto_schema(
        operation_summary="Получение списка команд",
        operation_description="Этот эндпоинт используется для получения списка всех команд.",
        responses=team_responses)

team_post_swagger = swagger_auto_schema(
        request_body=team_request_body,
        operation_summary="Создание команды",
        operation_description="Этот эндпоинт используется для создания новой команды.",
        responses={201: openapi.Response(description="Команда успешно создана", schema=TeamSerializer),
                   400: openapi.Response(description="", examples={'application/json': {'msg': 'serializers.errors'}})})