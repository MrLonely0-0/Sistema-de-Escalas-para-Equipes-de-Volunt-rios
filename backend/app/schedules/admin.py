"""
Admin configuration for schedules app
"""
from django.contrib import admin
from .models import (
    RegularSchedule, Event, ScheduleContent, GeneratedSchedule,
    Assignment, AssignmentHistory
)

@admin.register(RegularSchedule)
class RegularScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'day_of_week', 'start_time', 'end_time', 'frequency', 'is_active')
    list_filter = ('is_active', 'frequency', 'team')
    search_fields = ('name', 'team__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'team', 'event_date', 'start_time', 'end_time', 'is_urgent', 'status')
    list_filter = ('status', 'is_urgent', 'team')
    search_fields = ('title', 'team__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(ScheduleContent)
class ScheduleContentAdmin(admin.ModelAdmin):
    list_display = ('schedule_type', 'schedule_id', 'created_at')
    list_filter = ('schedule_type',)
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(GeneratedSchedule)
class GeneratedScheduleAdmin(admin.ModelAdmin):
    list_display = ('team', 'month', 'year', 'generated_by', 'status', 'created_at')
    list_filter = ('status', 'team', 'year', 'month')
    search_fields = ('team__name',)
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'schedule_date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'schedule_type')
    search_fields = ('user__email', 'role__name')
    readonly_fields = ('id', 'created_at', 'updated_at')

@admin.register(AssignmentHistory)
class AssignmentHistoryAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'old_status', 'new_status', 'changed_by', 'changed_at')
    list_filter = ('new_status',)
    search_fields = ('assignment__user__email',)
    readonly_fields = ('id', 'changed_at')
