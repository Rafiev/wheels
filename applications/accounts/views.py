from rest_framework import views, status
from django.contrib.auth import get_user_model
from applications.accounts.serializers import RegisterSerializer
from rest_framework.response import Response


User = get_user_model()


class RegisterApiView(views.APIView):

    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('You have successfully registered', status=status.HTTP_201_CREATED)