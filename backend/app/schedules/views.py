"""
Views for schedules app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from .models import (
    RegularSchedule, Event, ScheduleContent, GeneratedSchedule, Assignment
)
from .serializers import (
    RegularScheduleSerializer, EventSerializer, ScheduleContentSerializer,
    GeneratedScheduleSerializer, GeneratedScheduleDetailSerializer, AssignmentSerializer
)
from .algorithm import ScheduleGenerator

class RegularScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = RegularScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return RegularSchedule.objects.filter(team_id=team_id)
    
    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        serializer.save(team_id=team_id)

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return Event.objects.filter(team_id=team_id)
    
    def perform_create(self, serializer):
        team_id = self.kwargs.get('team_id')
        serializer.save(team_id=team_id)

class GeneratedScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = GeneratedScheduleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GeneratedScheduleDetailSerializer
        return GeneratedScheduleSerializer
    
    def get_queryset(self):
        team_id = self.kwargs.get('team_id')
        return GeneratedSchedule.objects.filter(team_id=team_id)
    
    @action(detail=False, methods=['post'])
    def generate(self, request, team_id=None):
        """Generate schedule for month/year"""
        month = request.data.get('month')
        year = request.data.get('year')
        
        if not month or not year:
            return Response({'error': 'month and year are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        from app.teams.models import Team
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'error': 'Team not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already exists
        existing = GeneratedSchedule.objects.filter(team=team, month=month, year=year).first()
        if existing:
            return Response(GeneratedScheduleDetailSerializer(existing).data)
        
        # Generate
        generator = ScheduleGenerator(team, month, year)
        assignments, schedule_data = generator.generate()
        
        generated = GeneratedSchedule.objects.create(
            team=team,
            month=month,
            year=year,
            schedule_data=schedule_data,
            generated_by=request.user,
            status='draft'
        )
        
        # Create assignments
        for assignment_data in assignments:
            Assignment.objects.create(
                generated_schedule=generated,
                **assignment_data
            )
        
        return Response(GeneratedScheduleDetailSerializer(generated).data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None, team_id=None):
        """Publish generated schedule"""
        schedule = self.get_object()
        schedule.status = 'published'
        schedule.published_at = datetime.now()
        schedule.save()
        
        # TODO: Trigger notifications for all assigned volunteers
        
        return Response(GeneratedScheduleDetailSerializer(schedule).data)

class AssignmentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Assignment.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm assignment"""
        assignment = self.get_object()
        assignment.status = 'confirmed'
        assignment.save()
        
        return Response(AssignmentSerializer(assignment).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel assignment"""
        assignment = self.get_object()
        assignment.status = 'cancelled'
        assignment.save()
        
        return Response(AssignmentSerializer(assignment).data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming assignments"""
        from datetime import datetime
        today = datetime.now().date()
        
        upcoming = Assignment.objects.filter(
            user=request.user,
            schedule_date__gte=today,
            status__in=['assigned', 'confirmed']
        ).order_by('schedule_date')
        
        serializer = AssignmentSerializer(upcoming, many=True)
        return Response(serializer.data)
