"""
Admin configuration for notifications app
"""
from django.contrib import admin
from .models import Notification, NotificationPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'channel', 'status', 'created_at')
    list_filter = ('type', 'channel', 'status')
    search_fields = ('user__email', 'title')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_enabled', 'whatsapp_enabled', 'push_enabled')
    list_filter = ('email_enabled', 'whatsapp_enabled', 'push_enabled')
    search_fields = ('user__email',)
    readonly_fields = ('id', 'updated_at')
