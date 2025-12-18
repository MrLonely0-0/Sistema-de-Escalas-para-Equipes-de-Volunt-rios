"""
Serializers for teams app
"""
from rest_framework import serializers
from app.users.serializers import UserSerializer
from .models import Team, TeamMember, Role, VolunteerRole, Availability

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'team', 'name', 'description', 'color', 'permissions', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

class TeamMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = TeamMember
        fields = ('id', 'user', 'team', 'role', 'status', 'joined_at', 'created_at')
        read_only_fields = ('id', 'created_at', 'joined_at')

class TeamSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'code', 'admin', 'members_count', 'created_at')
        read_only_fields = ('id', 'code', 'invite_link_token', 'created_at')
    
    def get_members_count(self, obj):
        return obj.members.filter(status='active').count()

class TeamDetailSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    members = TeamMemberSerializer(many=True, read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    members_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'code', 'invite_link_token', 'admin', 'members', 'roles', 'members_count', 'settings', 'created_at', 'updated_at')
        read_only_fields = ('id', 'code', 'invite_link_token', 'created_at', 'updated_at')
    
    def get_members_count(self, obj):
        return obj.members.filter(status='active').count()

class VolunteerRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    
    class Meta:
        model = VolunteerRole
        fields = ('id', 'volunteer', 'role', 'proficiency_level', 'created_at')
        read_only_fields = ('id', 'created_at')

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ('id', 'user', 'team', 'day_of_week', 'date', 'start_time', 'end_time', 'is_recurring', 'recurrence_pattern', 'created_at')
        read_only_fields = ('id', 'created_at')
