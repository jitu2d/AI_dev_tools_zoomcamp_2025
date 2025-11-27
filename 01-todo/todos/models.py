from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True, help_text="Set a due date for this task")
    reminder_date = models.DateTimeField(null=True, blank=True, help_text="Set a reminder for this task")
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def has_reminder(self):
        """Check if task has a reminder set"""
        return self.reminder_date is not None
    
    def is_reminder_upcoming(self):
        """Check if reminder is in the future"""
        if self.reminder_date:
            return self.reminder_date > timezone.now()
        return False
