"""
Admin configuration for users app
"""
from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_full_name', 'email', 'user_type', 'created_at')
    list_filter = ('user_type', 'email_verified', 'phone_verified')
    search_fields = ('email', 'first_name', 'last_name', 'phone')
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Identidade', {'fields': ('id', 'email', 'first_name', 'last_name')}),
        ('Contacto', {'fields': ('phone', 'phone_verified')}),
        ('Sistema', {'fields': ('user_type', 'email_verified', 'avatar_url')}),
        ('Datas', {'fields': ('created_at', 'updated_at')}),
    )
