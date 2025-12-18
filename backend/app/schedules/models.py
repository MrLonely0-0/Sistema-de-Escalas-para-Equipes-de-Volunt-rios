"""
Models for schedules app
"""
import uuid
from django.db import models
from app.users.models import User
from app.teams.models import Team, Role

class RegularSchedule(models.Model):
    FREQUENCY_CHOICES = (
        ('weekly', 'Semanal'),
        ('biweekly', 'Quinzenal'),
        ('monthly', 'Mensal'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='regular_schedules')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    day_of_week = models.IntegerField(choices=((i, f'Dia {i}') for i in range(7)))
    start_time = models.TimeField()
    end_time = models.TimeField()
    required_roles = models.JSONField(default=dict)  # {role_id: quantity}
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='weekly')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'regular_schedules'
        unique_together = ('team', 'day_of_week', 'start_time')
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.name} ({self.team})"

class Event(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('cancelled', 'Cancelado'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.TextField(blank=True, null=True)
    required_roles = models.JSONField(default=dict)  # {role_id: quantity}
    is_urgent = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'events'
        ordering = ['-event_date']
    
    def __str__(self):
        return f"{self.title} ({self.event_date})"

class ScheduleContent(models.Model):
    SCHEDULE_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('event', 'Evento'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule_id = models.UUIDField()
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPE_CHOICES)
    songs = models.JSONField(default=list)  # [{title, artist, key, link}]
    bible_passages = models.JSONField(default=list)  # [{book, chapter, verses, version}]
    attachments = models.JSONField(default=list)  # [{filename, url, type}]
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'schedule_content'
        unique_together = ('schedule_id', 'schedule_type')
    
    def __str__(self):
        return f"Content for {self.schedule_type} {self.schedule_id}"

class GeneratedSchedule(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='generated_schedules')
    month = models.IntegerField()
    year = models.IntegerField()
    schedule_data = models.JSONField()
    generation_algorithm = models.CharField(max_length=50, default='v1.0')
    generated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'generated_schedules'
        unique_together = ('team', 'month', 'year')
        ordering = ['-year', '-month']
    
    def __str__(self):
        return f"{self.team} - {self.month}/{self.year}"

class Assignment(models.Model):
    STATUS_CHOICES = (
        ('assigned', 'Atribuído'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado'),
        ('replaced', 'Substituído'),
    )
    SCHEDULE_TYPE_CHOICES = (
        ('regular', 'Regular'),
        ('event', 'Evento'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    generated_schedule = models.ForeignKey(GeneratedSchedule, on_delete=models.CASCADE, related_name='assignments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments')
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    schedule_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    schedule_type = models.CharField(max_length=20, choices=SCHEDULE_TYPE_CHOICES)
    schedule_reference_id = models.UUIDField(null=True, blank=True)  # ID do evento ou escala regular
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'assignments'
        unique_together = ('generated_schedule', 'user', 'schedule_date', 'role')
        ordering = ['-schedule_date']
    
    def __str__(self):
        return f"{self.user} - {self.role} ({self.schedule_date})"

class AssignmentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assignment_history_changed')
    old_status = models.CharField(max_length=50, null=True, blank=True)
    new_status = models.CharField(max_length=50)
    changed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assignment_changes')
    reason = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'assignment_history'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"History for {self.assignment}: {self.old_status} -> {self.new_status}"
