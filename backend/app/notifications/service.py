"""
Notification service for sending emails, WhatsApp, push, etc
"""
import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Notification

class NotificationService:
    @staticmethod
    def send_assignment_notification(assignment):
        """Send notification for new assignment"""
        user = assignment.user
        preferences = user.notification_preferences
        
        # Send email
        if preferences.email_enabled:
            NotificationService.send_email(
                user.email,
                f'Nova escala atribuída - {assignment.role.team.name}',
                f'Você foi escalado para {assignment.role.name} em {assignment.schedule_date}',
                assignment
            )
        
        # Send WhatsApp (simulated for now)
        if preferences.whatsapp_enabled and user.phone_verified:
            NotificationService.send_whatsapp(
                user.phone,
                f'Nova escala: {assignment.role.name} em {assignment.schedule_date}',
                assignment
            )
        
        # Create in-app notification
        Notification.objects.create(
            user=user,
            type='assignment',
            title='Nova Escala',
            message=f'Você foi escalado para {assignment.role.name} em {assignment.schedule_date}',
            metadata={'assignment_id': str(assignment.id)},
            channel='in_app',
            status='sent'
        )
    
    @staticmethod
    def send_email(to_email, subject, message, assignment=None):
        """Send email notification"""
        try:
            html_message = f"""
            <h2>{subject}</h2>
            <p>{message}</p>
            {f'<p>Hora: {assignment.start_time} - {assignment.end_time}</p>' if assignment else ''}
            {f'<p>Local: {assignment.role.description}</p>' if assignment else ''}
            """
            
            send_mail(
                subject,
                message,
                os.getenv('DEFAULT_FROM_EMAIL', 'noreply@escala.app'),
                [to_email],
                html_message=html_message,
                fail_silently=True
            )
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    @staticmethod
    def send_whatsapp(phone, message, assignment=None):
        """Send WhatsApp notification (mock for now)"""
        # TODO: Integrate with Twilio or WhatsApp Business API
        print(f"WhatsApp to {phone}: {message}")
        return True
    
    @staticmethod
    def schedule_reminders(assignment):
        """Schedule reminder notifications for assignment"""
        from celery import shared_task
        from datetime import timedelta
        from django.utils import timezone
        
        # 24 hours before
        reminder_24h = assignment.schedule_date - timedelta(days=1)
        reminder_24h_dt = timezone.make_aware(
            timezone.datetime.combine(reminder_24h, assignment.start_time)
        )
        
        # Same day at 8 AM
        day_of_dt = timezone.make_aware(
            timezone.datetime.combine(assignment.schedule_date, timezone.datetime.min.time().replace(hour=8))
        )
        
        # These would be scheduled with Celery beat
        # For now, we'll just create placeholder notifications
        Notification.objects.create(
            user=assignment.user,
            type='reminder',
            title='Lembrete: Sua escala é amanhã',
            message=f'Sua escala para {assignment.role.name} é amanhã às {assignment.start_time}',
            metadata={'assignment_id': str(assignment.id)},
            channel='email',
            status='pending',
            scheduled_for=reminder_24h_dt
        )
        
        Notification.objects.create(
            user=assignment.user,
            type='reminder',
            title='Lembrete: Sua escala é hoje',
            message=f'Sua escala para {assignment.role.name} é hoje às {assignment.start_time}',
            metadata={'assignment_id': str(assignment.id)},
            channel='email',
            status='pending',
            scheduled_for=day_of_dt
        )
