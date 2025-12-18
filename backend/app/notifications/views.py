"""
Views for notifications app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import Notification, NotificationPreference
from .serializers import NotificationSerializer, NotificationDetailSerializer, NotificationPreferenceSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.status = 'read'
        notification.read_at = datetime.now()
        notification.save()
        
        return Response(NotificationDetailSerializer(notification).data)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications"""
        unread = Notification.objects.filter(user=request.user, status__in=['pending', 'sent'])
        serializer = NotificationSerializer(unread, many=True)
        return Response(serializer.data)

class NotificationPreferenceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def get_preferences(self, request):
        """Get notification preferences for authenticated user"""
        pref, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(pref)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def set_preferences(self, request):
        """Update notification preferences"""
        pref, created = NotificationPreference.objects.get_or_create(user=request.user)
        serializer = NotificationPreferenceSerializer(pref, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
