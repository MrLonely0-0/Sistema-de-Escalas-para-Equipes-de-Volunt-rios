"""
Schedule generation algorithm
"""
from datetime import datetime, timedelta
from collections import defaultdict
from app.teams.models import Role, VolunteerRole, Availability
from .models import Assignment, GeneratedSchedule

class ScheduleGenerator:
    def __init__(self, team, month, year):
        self.team = team
        self.month = month
        self.year = year
    
    def generate(self):
        """Main schedule generation logic"""
        volunteers = self._get_available_volunteers()
        regular_schedules = self.team.regular_schedules.filter(is_active=True)
        events = self.team.events.filter(status='published', event_date__month=self.month, event_date__year=self.year)
        
        assignments = []
        
        # Process regular schedules
        for regular in regular_schedules:
            dates = self._get_dates_for_regular_schedule(regular)
            for date in dates:
                role_assignments = self._assign_for_date(
                    volunteers, date, regular.required_roles, 'regular', regular.id
                )
                assignments.extend(role_assignments)
        
        # Process events
        for event in events:
            role_assignments = self._assign_for_date(
                volunteers, event.event_date, event.required_roles, 'event', event.id
            )
            assignments.extend(role_assignments)
        
        # Balance assignments
        self._balance_assignments(volunteers, assignments)
        
        schedule_data = {
            'month': self.month,
            'year': self.year,
            'total_assignments': len(assignments),
            'volunteers_count': len(volunteers),
        }
        
        return assignments, schedule_data
    
    def _get_available_volunteers(self):
        """Get volunteers with their stats"""
        volunteers = []
        team_members = self.team.members.filter(status='active')
        
        for member in team_members:
            volunteer = member.user
            roles = list(VolunteerRole.objects.filter(volunteer=volunteer).values_list('role_id', flat=True))
            
            assignment_count = Assignment.objects.filter(
                user=volunteer,
                schedule_date__month=self.month,
                schedule_date__year=self.year
            ).count()
            
            last_assignment = Assignment.objects.filter(user=volunteer).order_by('-schedule_date').first()
            
            volunteers.append({
                'id': volunteer.id,
                'user': volunteer,
                'roles': roles,
                'assignments_count': assignment_count,
                'last_assignment': last_assignment.schedule_date if last_assignment else None,
                'priority_score': 1.0,
            })
        
        return volunteers
    
    def _get_dates_for_regular_schedule(self, regular):
        """Get dates for regular schedule in month"""
        dates = []
        start_date = datetime(self.year, self.month, 1).date()
        
        # Get last day of month
        if self.month == 12:
            end_date = datetime(self.year + 1, 1, 1).date() - timedelta(days=1)
        else:
            end_date = datetime(self.year, self.month + 1, 1).date() - timedelta(days=1)
        
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() == regular.day_of_week:
                dates.append(current_date)
            current_date += timedelta(days=1)
        
        return dates
    
    def _assign_for_date(self, volunteers, date, required_roles, schedule_type, schedule_id):
        """Assign volunteers for specific date"""
        assignments = []
        
        for role_id, quantity in required_roles.items():
            candidates = self._get_candidates(volunteers, role_id, date)
            selected = sorted(candidates, key=lambda x: (
                x['assignments_count'],
                x['last_assignment'] or date,
                -x['priority_score']
            ))[:quantity]
            
            for volunteer in selected:
                # Get regular schedule or event details
                if schedule_type == 'regular':
                    from .models import RegularSchedule
                    schedule = RegularSchedule.objects.get(id=schedule_id)
                    start_time = schedule.start_time
                    end_time = schedule.end_time
                elif schedule_type == 'event':
                    from .models import Event
                    event = Event.objects.get(id=schedule_id)
                    start_time = event.start_time
                    end_time = event.end_time
                
                role = Role.objects.get(id=role_id)
                
                assignment = {
                    'user': volunteer['user'],
                    'role': role,
                    'schedule_date': date,
                    'start_time': start_time,
                    'end_time': end_time,
                    'schedule_type': schedule_type,
                    'schedule_reference_id': schedule_id,
                }
                assignments.append(assignment)
                volunteer['assignments_count'] += 1
        
        return assignments
    
    def _get_candidates(self, volunteers, role_id, date):
        """Get available candidates for role on date"""
        candidates = []
        
        for volunteer in volunteers:
            # Check if has role
            if role_id not in volunteer['roles']:
                continue
            
            # Check availability
            if not self._is_available(volunteer['user'], date):
                continue
            
            candidates.append(volunteer)
        
        return candidates
    
    def _is_available(self, user, date):
        """Check if user is available on date"""
        availability = Availability.objects.filter(user=user, team=self.team)
        
        if not availability.exists():
            return True
        
        # Check specific date
        specific = availability.filter(date=date, is_recurring=False).first()
        if specific:
            return True
        
        # Check recurring for day of week
        recurring = availability.filter(
            day_of_week=date.weekday(),
            is_recurring=True
        ).first()
        
        return recurring is not None
    
    def _balance_assignments(self, volunteers, assignments):
        """Balance assignments to ensure fairness"""
        # Count assignments per volunteer
        counts = defaultdict(int)
        for assignment in assignments:
            counts[assignment['user'].id] += 1
        
        # Check imbalances (simple version - could be more sophisticated)
        if counts:
            max_count = max(counts.values())
            min_count = min(counts.values())
            if max_count - min_count > 2:
                # Log warning for manual review
                pass
