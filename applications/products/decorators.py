from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from applications.products.serializers import AcceptanceListSerializer, StorageSerializer, WheelListSerializer, \
    WheelSerializer

acceptance_post_swagger = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    'season': openapi.Schema(type=openapi.TYPE_STRING),
                    'storage': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'wheels': openapi.Schema(type=openapi.TYPE_ARRAY,
                                             items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                  properties={
                                                                      'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                      'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                  })),
                    'new_wheels': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                                                                      'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                      'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                        }))},
        required=['created_at', 'storage', 'wheels']),
    responses={
        201: openapi.Response(description="",
                              examples={'application/json': {'msg': 'Ваша приемка успешно добавлена'}}),
        400: openapi.Response(description=" ",
                              examples={'application/json': {'msg': 'serializer.error'}})},
    operation_summary="Добавление приемки",
    operation_description="Этот эндпоинт используется для добавления новой приемки.")

acceptance_get_swagger = swagger_auto_schema(
    operation_summary="Получение списка приемок",
    operation_description="Этот эндпоинт возвращает список приемок с возможностью фильтрации по дате и месту хранения.",
    manual_parameters=[
        openapi.Parameter(
            name="start_date",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False,
            description="Начальная дата для фильтрации (в формате 'YYYY-MM-DD')"
        ),
        openapi.Parameter(
            name="end_date",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            required=False,
            description="Конечная дата для фильтрации (в формате 'YYYY-MM-DD')"
        ),
        openapi.Parameter(
            name="storage_id",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description="Идентификатор места хранения для фильтрации"
        ),
        openapi.Parameter(
            name="season",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description="Время года для фильтрации"
        )
    ],
    responses={200: openapi.Response(description="",
                                     examples={"application/json": [{"id": 33, "created_at": "2024-02-04",
                                                                     "user": "rafievvv@gmail.com",
                                                                     "storage": {"id": 5,
                                                                                 "title": "Контейнер",
                                                                                 "owner": "Team_1",
                                                                                 "parent": None},
                                                                     "amount": 90},
                                                                    {"id": 34, "created_at": "2024-03-02",
                                                                     "user": "rafievvv@gmail.com",
                                                                     "storage": {"id": 5,
                                                                                 "title": "Контейнер",
                                                                                 "owner": "Team_1",
                                                                                 "parent": None},
                                                                     "amount": 90}]})})

acceptance_get_detail_swagger = swagger_auto_schema(
    operation_summary="Получение деталей приемки",
    operation_description="Этот эндпоинт возвращает детали приемки по ее идентификатору.",
    responses={
        200: openapi.Response(description="", schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "storage": openapi.Schema(type=openapi.TYPE_OBJECT,
                                                  properties={"id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                                              "title": openapi.Schema(type=openapi.TYPE_STRING),
                                                              "owner": openapi.Schema(type=openapi.TYPE_STRING),
                                                              "parent": openapi.Schema(type=openapi.TYPE_STRING,
                                                                                       default=None)
                                                              }),
                        "created_at": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                        "wheels": openapi.Schema(type=openapi.TYPE_ARRAY,
                                                 items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                      properties={
                                                                          "title": openapi.Schema(
                                                                              type=openapi.TYPE_STRING),
                                                                          "amount": openapi.Schema(
                                                                              type=openapi.TYPE_INTEGER),
                                                                      })),
                        "user": openapi.Schema(type=openapi.TYPE_STRING),
                        "season": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner": openapi.Schema(type=openapi.TYPE_STRING)})),
        400: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})})

acceptance_delete_swagger = swagger_auto_schema(
    operation_summary="Удаление приемки",
    operation_description="Этот эндпоинт удаляет приемку по ее идентификатору.",
    responses={
        204: openapi.Response(description="", examples={"application/json": {"msg": "Объект успешно удален"}}),
        401: openapi.Response(description="", examples={"application/json": {"msg": "У вас нет прав на это"}}),
        404: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})
    }
)

storage_post_swagger = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title'],
        ),
        operation_summary="Создание хранилища",
        operation_description="Этот эндпоинт используется для создания нового хранилища.",
        responses={
            201: openapi.Response(description="", examples={"application/json": {"id": 11,
                                                                                 "title": openapi.TYPE_STRING,
                                                                                 "owner": "Team_1",
                                                                                 "parent": None}}),
            400: openapi.Response(description="", examples={"application/json": {"msg": "serializers.errors"}}),
            401: openapi.Response(description="", examples={"application/json": {"msg": "У вас нет прав на это"}}),
        }
    )

storage_get_swagger = swagger_auto_schema(
        operation_summary="Получение списка хранилищ",
        operation_description="Этот эндпоинт используется для получения списка всех хранилищ, принадлежащих текущей команде.",
        responses={200: openapi.Response(description="", examples={"application/json": [
            {"id": openapi.TYPE_INTEGER,
             "title": openapi.TYPE_STRING,
             "owner": openapi.TYPE_STRING,
             "parent": None},
            {"id": openapi.TYPE_INTEGER,
             "title": openapi.TYPE_STRING,
             "owner": openapi.TYPE_STRING,
             "parent": None}]})})

storage_delete_swagger = swagger_auto_schema(
    operation_summary="Удаление хранилища",
    operation_description="Этот эндпоинт используется для удаления хранилища по его идентификатору.",
    responses={
        204: openapi.Response(description="", examples={"application/json": {"msg": "Хранилище успешно удалено"}}),
        401: openapi.Response(description="", examples={"application/json": {"msg": "У вас нет прав на это"}}),
        404: openapi.Response(description="", examples={"application/json": {"msg": "Хранилище не найдено"}})
    }
    )

storage_get_detail_swagger = swagger_auto_schema(
        operation_summary="Получение списка колес",
        operation_description="Этот эндпоинт используется для получения списка всех колес, принадлежащих указанному хранилищу.",
        manual_parameters=[openapi.Parameter(name='search',
                                             in_=openapi.IN_QUERY,
                                             type=openapi.TYPE_STRING,
                                             required=False,
                                             description='Строка для поиска по названию колеса'),
                           openapi.Parameter(name='season',
                                             in_=openapi.IN_QUERY,
                                             type=openapi.TYPE_STRING,
                                             required=False,
                                             description='Строка для фильтрации по сезону')
                           ],
        responses={200: openapi.Response(description="", schema=WheelListSerializer(many=True))})

wheel_post_swagger = swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                'storage': openapi.Schema(type=openapi.TYPE_INTEGER),
                'title': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['title', 'amount', 'storage'],
        ),
        operation_summary="Создание колеса",
        operation_description="Этот эндпоинт используется для создания нового колеса.",
        responses={
            201: openapi.Response(description="", examples={"application/json": {"id": 0,
                                                                                 "title": "string",
                                                                                 "amount": 0,
                                                                                 "price": "0.00",
                                                                                 "owner": "string",
                                                                                 "storage": 0}}),
            400: openapi.Response(description="", examples={"application/json": {"msg": "serializers.errors"}}),
        }
    )

wheel_delete_swagger = swagger_auto_schema(
    operation_summary="Удаление колеса",
    operation_description="Этот эндпоинт используется для удаления колеса по его идентификатору.",
    responses={
        204: openapi.Response(description="", examples={"application/json": {"msg": "Объект успешно удален"}}),
        401: openapi.Response(description="", examples={"application/json": {"msg": "У вас нет прав на это"}}),
        404: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})
    }
    )

wheel_get_detail_swagger = swagger_auto_schema(
        operation_summary="Получение детальной информации колеса",
        operation_description="Этот эндпоинт используется для получения всей информации о колесе по id.",
        responses={200: openapi.Response(description="", examples={"application/json": {"id": 0,
                                                                                        "storage": {
                                                                                            "id": 0,
                                                                                            "title": "string",
                                                                                            "owner": "string",
                                                                                            "parent": None},
                                                                                        "title": "string",
                                                                                        "amount": 0,
                                                                                        "price": "0.00",
                                                                                        "owner": "string"}}),
                   404: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})})

wheel_put_swagger = swagger_auto_schema(
        operation_summary="Обновление информации о колесе",
        operation_description="Этот эндпоинт используется для обновления информации о колесе.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING),
                'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={
            200: openapi.Response(description="", examples={"application/json": {"id": 0,
                                                                                 "title": "string",
                                                                                 "amount": 0,
                                                                                 "price": "0.00",
                                                                                 "owner": "string",
                                                                                 "storage": 0}}),
            400: openapi.Response(description="", examples={"application/json": {"msg": "serializers.errors"}}),
            404: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})
        }
    )