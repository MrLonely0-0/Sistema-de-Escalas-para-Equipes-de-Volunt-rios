"""
Models for notifications app
"""
import uuid
from django.db import models
from app.users.models import User
from app.schedules.models import Assignment

class Notification(models.Model):
    TYPE_CHOICES = (
        ('assignment', 'Atribuição'),
        ('reminder', 'Lembrete'),
        ('system', 'Sistema'),
        ('team', 'Equipe'),
    )
    CHANNEL_CHOICES = (
        ('email', 'E-mail'),
        ('whatsapp', 'WhatsApp'),
        ('push', 'Push'),
        ('in_app', 'In-app'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('sent', 'Enviado'),
        ('failed', 'Falhou'),
        ('read', 'Lido'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    metadata = models.JSONField(default=dict)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user}"

class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_enabled = models.BooleanField(default=True)
    whatsapp_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    reminders_24h = models.BooleanField(default=True)
    reminders_day_of = models.BooleanField(default=True)
    assignment_notifications = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'notification_preferences'
    
    def __str__(self):
        return f"Preferences for {self.user}"
