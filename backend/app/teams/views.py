"""
Views for teams app
"""
import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import models as db_models
from .models import Team, TeamMember, Role, VolunteerRole, Availability
from .serializers import (
    TeamSerializer, TeamDetailSerializer, TeamMemberSerializer,
    RoleSerializer, VolunteerRoleSerializer, AvailabilitySerializer
)

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Team.objects.filter(
            db_models.Q(admin=user) | db_models.Q(members__user=user)
        ).distinct()
    
    def perform_create(self, serializer):
        code = str(uuid.uuid4())[:10].upper()
        token = str(uuid.uuid4())
        serializer.save(admin=self.request.user, code=code, invite_link_token=token)
    
    @action(detail=True, methods=['post'])
    def invite(self, request, pk=None):
        """Convidar usuário para equipe"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from app.users.models import User
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        member, created = TeamMember.objects.get_or_create(
            user=user, team=team, defaults={'status': 'pending'}
        )
        
        if not created and member.status != 'pending':
            return Response({'error': 'User is already a member'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(TeamMemberSerializer(member).data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['post'])
    def join(self, request):
        """Unir-se a equipe com código ou token"""
        code = request.data.get('code')
        token = request.data.get('token')
        
        if not code and not token:
            return Response({'error': 'code or token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if code:
                team = Team.objects.get(code=code)
            else:
                team = Team.objects.get(invite_link_token=token)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        
        member, created = TeamMember.objects.get_or_create(
            user=request.user, team=team, defaults={'status': 'active'}
        )
        
        if not created:
            member.status = 'active'
            member.save()
        
        return Response(TeamMemberSerializer(member).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class RoleViewSet(viewsets.ModelViewSet):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return Role.objects.filter(team_id=team_id)
    
    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        serializer.save(team_id=team_id)

class VolunteerRoleViewSet(viewsets.ModelViewSet):
    serializer_class = VolunteerRoleSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def my_roles(self, request):
        """Obter funções do voluntário autenticado"""
        roles = VolunteerRole.objects.filter(volunteer=request.user)
        serializer = VolunteerRoleSerializer(roles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_role(self, request):
        """Adicionar função ao voluntário"""
        role_id = request.data.get('role_id')
        
        if not role_id:
            return Response({'error': 'role_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        
        vol_role, created = VolunteerRole.objects.get_or_create(
            volunteer=request.user, role=role, 
            defaults={'proficiency_level': request.data.get('proficiency_level', 1)}
        )
        
        if not created:
            vol_role.proficiency_level = request.data.get('proficiency_level', vol_role.proficiency_level)
            vol_role.save()
        
        return Response(VolunteerRoleSerializer(vol_role).data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Availability.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
