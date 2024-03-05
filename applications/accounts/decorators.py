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
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'password': openapi.Schema(type=openapi.TYPE_STRING),
                    'role': openapi.Schema(type=openapi.TYPE_STRING),
                    'team': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'functions': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(
                                                type=openapi.TYPE_OBJECT,
                                                properties={
                                                    'Создание приемки': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                                    'Создание продаж': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                                    'Возврат': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                                    'Брак': openapi.Schema(type=openapi.TYPE_BOOLEAN),}))},
        required=['email', 'password', 'role', 'team', 'functions']),
    responses={201: openapi.Response(description="",  examples={'application/json': {"id": 4, "email": "Jhon@а.com",
                                                                                     "role": "Worker",
                                                                                     "team": 1,
                                                                                     "functions": {
                                                                                            "Создание приемки": True,
                                                                                            "Создание продаж": False,
                                                                                            "Возврат": False,
                                                                                            "Брак": True}}}),
               400: openapi.Response(description="",  examples={'application/json': {'msg': 'serializers.errors'}}),
               409: openapi.Response(description="",  examples={'application/json': {'msg': 'У вас нет прав на это'}})},
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
            200: openapi.Response(description="Список пользователей команды",
                                  examples={'application/json': [{"id": 2, "email": "rafiev@g.com", "role": "Owner",
                                                                  "team": 1,
                                                                  "functions": {"Брак": True,
                                                                                "Возврат": True,
                                                                                "Создание продаж": True,
                                                                                "Создание приемки": True}},
                                                                 {"id": 4, "email": "JhonSnow@а.com", "role": "Worker",
                                                                  "team": 1,
                                                                  "functions": {"Брак": True,
                                                                                "Возврат": False,
                                                                                "Создание продаж": True,
                                                                                "Создание приемки": True}}]}),
            409: openapi.Response(
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


profile_swagger = swagger_auto_schema(
        operation_summary="Информация о пользователе профиль",
        operation_description="Этот эндпоинт используется для получения профиля юзера.",
        responses={200: openapi.Response(description="",
                                         examples={'application/json': {"id": 2, "email": "rafiev@g.com",
                                                                        "role": "Owner",
                                                                        "team": 1,
                                                                        "functions": {"Брак": True,
                                                                                      "Возврат": True,
                                                                                      "Создание продаж": True,
                                                                                      "Создание приемки": True}}})})


user_active_change = swagger_auto_schema(
    request_body=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING)},
                                  required=['title']),
    responses={200: openapi.Response(description="", examples={'application/json': {'msg': 'Пользователи актевированы'}}),
               400: openapi.Response(description="", examples={'application/json': {'msg': 'Название команды не указано'}}),
               404: openapi.Response(description="", examples={'application/json': {'msg': 'Команда не найдена'}}),
               204: openapi.Response(description="", examples={'application/json': {'msg': 'Пользователи отключены'}})},
    operation_summary="Отключения включения пользователя",
)