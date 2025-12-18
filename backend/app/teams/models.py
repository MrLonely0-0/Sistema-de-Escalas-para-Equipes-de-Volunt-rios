"""
Models for teams app
"""
import uuid
from django.db import models
from app.users.models import User

class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    code = models.CharField(max_length=10, unique=True)
    invite_link_token = models.CharField(max_length=50, unique=True)
    admin = models.ForeignKey(User, on_delete=models.PROTECT, related_name='admin_teams')
    settings = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class TeamMember(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
    )
    ROLE_CHOICES = (
        ('volunteer', 'Voluntário'),
        ('admin', 'Administrador'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='team_memberships')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='volunteer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    joined_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'team_members'
        unique_together = ('user', 'team')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user} in {self.team}"

class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='roles')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#000000')
    permissions = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        unique_together = ('team', 'name')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.team})"

class VolunteerRole(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='volunteers')
    proficiency_level = models.IntegerField(default=1, choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'volunteer_roles'
        unique_together = ('volunteer', 'role')
        ordering = ['-proficiency_level']
    
    def __str__(self):
        return f"{self.volunteer} - {self.role}"

class Availability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.IntegerField(null=True, blank=True, choices=((i, f'Dia {i}') for i in range(7)))
    date = models.DateField(null=True, blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_recurring = models.BooleanField(default=True)
    recurrence_pattern = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'availability'
        ordering = ['-created_at']
    
    def __str__(self):
        if self.is_recurring:
            return f"{self.user} - {self.get_day_of_week_display()}"
        return f"{self.user} - {self.date}"
