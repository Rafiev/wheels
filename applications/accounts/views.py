from rest_framework import views, status
from django.contrib.auth import get_user_model
from applications.accounts.serializers import CustomUserSerializer, TeamSerializer
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

