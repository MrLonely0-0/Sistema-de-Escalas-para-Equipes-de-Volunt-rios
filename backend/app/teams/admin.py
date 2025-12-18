"""
Admin configuration for teams app
"""
from django.contrib import admin
from .models import Team, TeamMember, Role, VolunteerRole, Availability

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'admin', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('id', 'code', 'invite_link_token', 'created_at', 'updated_at')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'role', 'status', 'created_at')
    list_filter = ('status', 'role')
    search_fields = ('user__email', 'team__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'color', 'is_active', 'created_at')
    list_filter = ('is_active', 'team')
    search_fields = ('name', 'team__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(VolunteerRole)
class VolunteerRoleAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'role', 'proficiency_level')
    search_fields = ('volunteer__email', 'role__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'day_of_week', 'date', 'start_time', 'end_time')
    list_filter = ('is_recurring', 'team')
    search_fields = ('user__email', 'team__name')
    readonly_fields = ('id', 'created_at', 'updated_at')
