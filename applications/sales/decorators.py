from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

sale_post_swagger = swagger_auto_schema(
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
                                                                      'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                  }))},
        required=['created_at', 'storage', 'wheels']),
    responses={
        201: openapi.Response(description="",
                              examples={'application/json': {'msg': 'Ваша продажа успешно добавлена'}}),
        400: openapi.Response(description=" ",
                              examples={'application/json': {'msg': 'serializer.error'}})},
    operation_summary="Добавление продажи",
    operation_description="Этот эндпоинт используется для добавления новой продажи.")


defect_post_swagger = swagger_auto_schema(
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
                                                                  }))},
        required=['created_at', 'storage', 'wheels']),
    responses={
        201: openapi.Response(description="",
                              examples={'application/json': {'msg': 'Ваш брак успешно добавлен'}}),
        400: openapi.Response(description=" ",
                              examples={'application/json': {'msg': 'serializer.error'}})},
    operation_summary="Добавление брака",
    operation_description="Этот эндпоинт используется для добавления нового брака.")


return_post_swagger = swagger_auto_schema(
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
                                                                  }))},
        required=['created_at', 'storage', 'wheels']),
    responses={
        201: openapi.Response(description="",
                              examples={'application/json': {'msg': 'Ваш возврат успешно добавлен'}}),
        400: openapi.Response(description=" ",
                              examples={'application/json': {'msg': 'serializer.error'}})},
    operation_summary="Добавление возврата",
    operation_description="Этот эндпоинт используется для добавления нового возврата.")


action_get_swagger = swagger_auto_schema(
    operation_summary="Получение списка действий",
    operation_description="Этот эндпоинт возвращает список дейтсвий с возможностью фильтрации по дате, месту хранения, "
                          "типу действия и времени года.",
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
        ),
        openapi.Parameter(
            name="action_type",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            required=False,
            description="Тип действия для фильтрации"
        )
    ],

    responses={200: openapi.Response(description="",
                                     examples={"application/json": [{"id": 8, "created_at": "2024-03-30",
                                                                     "user": "rafiev@g.com",
                                                                     "storage": {"id": 1,
                                                                                 "title": "Контейнер",
                                                                                 "owner": "teenwolf",
                                                                                 "parent": None,
                                                                                 "amount": 297},
                                                                     "action_type": "Возврат",
                                                                     "amount": 3},
                                                                    {"id": 9, "created_at": "2024-03-10",
                                                                     "user": "rafiev@g.com",
                                                                     "storage": {"id": 1,
                                                                                 "title": "Контейнер",
                                                                                 "owner": "teenwolf",
                                                                                 "parent": None,
                                                                                 "amount": 297},
                                                                     "action_type": "Возврат",
                                                                     "amount": 3}]})})

action_get_detail_swagger = swagger_auto_schema(
    operation_summary="Получение деталей действия",
    operation_description="Этот эндпоинт возвращает детали действия по ее идентификатору.",
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
                                                                          "id": openapi.Schema(
                                                                              type=openapi.TYPE_INTEGER),
                                                                          "title": openapi.Schema(
                                                                              type=openapi.TYPE_STRING),
                                                                          "amount": openapi.Schema(
                                                                              type=openapi.TYPE_INTEGER),
                                                                          "price": openapi.Schema(
                                                                              type=openapi.TYPE_INTEGER),
                                                                          "total-cost": openapi.Schema(
                                                                              type=openapi.TYPE_INTEGER
                                                                          )
                                                                      })),
                        "user": openapi.Schema(type=openapi.TYPE_STRING),
                        "season": openapi.Schema(type=openapi.TYPE_STRING),
                        "action_type": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner": openapi.Schema(type=openapi.TYPE_STRING)})),
        400: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})})

action_delete_swagger = swagger_auto_schema(
    operation_summary="Удаление действия",
    operation_description="Этот эндпоинт удаляет действие по ее идентификатору.",
    responses={
        204: openapi.Response(description="", examples={"application/json": {"msg": "Объект успешно удален"}}),
        401: openapi.Response(description="", examples={"application/json": {"msg": "У вас нет прав на это"}}),
        404: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})
    }
)
