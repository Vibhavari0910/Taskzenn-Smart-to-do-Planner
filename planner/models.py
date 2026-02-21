from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    # Priority Choices
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    # Status Choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES
    )

    deadline = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def str(self):
        return self.title
