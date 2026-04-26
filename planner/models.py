from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta


class Task(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Study', 'Study'),
        ('Personal', 'Personal'),
        ('Health', 'Health'),
        ('Finance', 'Finance'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Work')

    deadline = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.title

    @property
    def is_overdue(self):
        if self.deadline is None:
            return False
        return self.deadline < timezone.now().date() and self.status == 'Pending'
    
    @property
    def is_due_soon(self):
        if self.status == "Completed":
            return False
        if self.deadline:
           return self.deadline in [date.today(), date.today() + timedelta(days=1)]
           return False