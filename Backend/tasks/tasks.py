from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_due_date_reminders(self) -> None:
    try:
        tomorrow = timezone.now().date() + timedelta(days=1)
        due_tasks = Task.objects.filter(due_on=tomorrow, completed__in=['to_do', 'in_progress'], reminder_sent=False)
        for task in due_tasks:
            print(f"REMINDER: Task '{task.title}' (owner: {task.owner.username}) is due tomorrow")
            task.reminder_sent = True
            task.save()
    except Exception as exc:
        raise self.retry(exc=exc)
    
