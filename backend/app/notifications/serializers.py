"""
Serializers for notifications app
"""
from rest_framework import serializers
from app.users.serializers import UserSerializer
from .models import Notification, NotificationPreference

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'type', 'title', 'message', 'channel', 'status', 'scheduled_for', 'sent_at', 'read_at', 'created_at')
        read_only_fields = ('id', 'status', 'sent_at', 'created_at')

class NotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'user', 'type', 'title', 'message', 'metadata', 'channel', 'status', 'scheduled_for', 'sent_at', 'read_at', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'status', 'sent_at', 'created_at', 'updated_at')

class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationPreference
        fields = ('id', 'email_enabled', 'whatsapp_enabled', 'push_enabled', 'reminders_24h', 'reminders_day_of', 'assignment_notifications', 'updated_at')
        read_only_fields = ('id', 'updated_at')
