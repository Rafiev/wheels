from rest_framework import views, status
from django.contrib.auth import get_user_model
from applications.accounts.serializers import RegisterSerializer, CustomUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Team

User = get_user_model()


class GetTeamAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(self, request, *args, **kwargs):

        if not request.user.role == 'Owner':
            return Response({'msg': 'You do not have the right to do this'}, status=status.HTTP_401_UNAUTHORIZED)
        user_team = User.objects.filter(team_id=request.user.team_id)
        serializer = CustomUserSerializer(user_team, many=True)

        return Response(serializer.data)


class RegisterAPIView(views.APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'You have successfully registered'}, status=status.HTTP_201_CREATED)
        return Response({'msg': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

