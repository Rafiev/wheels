from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

sale_post_swagger = swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
                    'storage': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'wheels': openapi.Schema(type=openapi.TYPE_ARRAY,
                                             items=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                                  properties={
                                                                      'title': openapi.Schema(type=openapi.TYPE_STRING),
                                                                      'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                      'price': openapi.Schema(type=openapi.TYPE_INTEGER),
                                                                      'season': openapi.Schema(type=openapi.TYPE_STRING)
                                                                  }))},
        required=['created_at', 'storage', 'wheels']),
    responses={
        201: openapi.Response(description="",
                              examples={'application/json': {'msg': 'Ваша продажа успешно добавлена'}}),
        400: openapi.Response(description=" ",
                              examples={'application/json': {'msg': 'serializer.error'}})},
    operation_summary="Добавление продажи",
    operation_description="Этот эндпоинт используется для добавления новой приемки.")

sale_get_swagger = swagger_auto_schema(
    operation_summary="Получение списка продаж",
    operation_description="Этот эндпоинт возвращает список продаж с возможностью фильтрации по дате и месту хранения.",
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
        )
    ],
    responses={200: openapi.Response(description="",
                                     examples={"application/json":     [{"id": 54, "created_at": "2024-02-24",
                                                                         "user": "rafievvv@gmail.com",
                                                                         "storage": {"id": 6, "title": "Cклад",
                                                                                     "owner": "Team_1", "parent": None,
                                                                                     "amount": 0},
                                                                         "amount": 70, "total-cost": 21140},
                                                                        {"id": 53, "created_at": "2024-02-24",
                                                                         "user": "rafievvv@gmail.com",
                                                                         "storage": {"id": 6, "title": "Cклад",
                                                                                     "owner": "Team_1", "parent": None,
                                                                                     "amount": 0},
                                                                         "amount": 70, "total-cost": 21140}]})})

sale_get_detail_swagger = swagger_auto_schema(
    operation_summary="Получение деталей продажи",
    operation_description="Этот эндпоинт возвращает детали продажи по ее идентификатору.",
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
                                                                          "season": openapi.Schema(
                                                                              type=openapi.TYPE_STRING),
                                                                          "total-cost": openapi.Schema(
                                                                              type=openapi.TYPE_INTEGER
                                                                          )
                                                                      })),
                        "user": openapi.Schema(type=openapi.TYPE_STRING),
                        "owner": openapi.Schema(type=openapi.TYPE_STRING)})),
        400: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})})

sale_delete_swagger = swagger_auto_schema(
    operation_summary="Удаление продажи",
    operation_description="Этот эндпоинт удаляет продажу по ее идентификатору.",
    responses={
        204: openapi.Response(description="", examples={"application/json": {"msg": "Объект успешно удален"}}),
        401: openapi.Response(description="", examples={"application/json": {"msg": "У вас нет прав на это"}}),
        404: openapi.Response(description="", examples={"application/json": {"msg": "Объект не найден"}})
    }
)
