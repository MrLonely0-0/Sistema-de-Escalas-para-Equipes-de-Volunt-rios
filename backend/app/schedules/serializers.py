"""
Serializers for schedules app
"""
from rest_framework import serializers
from app.users.serializers import UserSerializer
from app.teams.serializers import RoleSerializer
from .models import (
    RegularSchedule, Event, ScheduleContent, GeneratedSchedule,
    Assignment, AssignmentHistory
)

class RegularScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularSchedule
        fields = ('id', 'team', 'name', 'description', 'day_of_week', 'start_time', 'end_time', 'required_roles', 'frequency', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'team', 'title', 'description', 'event_date', 'start_time', 'end_time', 'location', 'required_roles', 'is_urgent', 'status', 'created_at')
        read_only_fields = ('id', 'created_at')

class ScheduleContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleContent
        fields = ('id', 'schedule_id', 'schedule_type', 'songs', 'bible_passages', 'attachments', 'notes', 'created_at')
        read_only_fields = ('id', 'created_at')

class AssignmentHistorySerializer(serializers.ModelSerializer):
    changed_by = UserSerializer(read_only=True)
    
    class Meta:
        model = AssignmentHistory
        fields = ('id', 'old_status', 'new_status', 'changed_by', 'reason', 'changed_at')
        read_only_fields = ('id', 'changed_at')

class AssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    history = AssignmentHistorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Assignment
        fields = ('id', 'user', 'role', 'schedule_date', 'start_time', 'end_time', 'schedule_type', 'schedule_reference_id', 'status', 'notes', 'history', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at', 'history')

class GeneratedScheduleSerializer(serializers.ModelSerializer):
    generated_by = UserSerializer(read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = GeneratedSchedule
        fields = ('id', 'team', 'month', 'year', 'schedule_data', 'generation_algorithm', 'generated_by', 'status', 'published_at', 'assignments', 'created_at', 'updated_at')
        read_only_fields = ('id', 'schedule_data', 'generated_by', 'created_at', 'updated_at', 'published_at', 'assignments')

class GeneratedScheduleDetailSerializer(serializers.ModelSerializer):
    generated_by = UserSerializer(read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = GeneratedSchedule
        fields = ('id', 'team', 'month', 'year', 'schedule_data', 'generation_algorithm', 'generated_by', 'status', 'published_at', 'assignments', 'created_at', 'updated_at')
        read_only_fields = ('id', 'schedule_data', 'generated_by', 'created_at', 'updated_at', 'published_at')
