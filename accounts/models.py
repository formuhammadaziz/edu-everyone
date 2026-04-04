from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    target_band_score = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    exam_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.username

    @property
    def days_until_exam(self):
        if self.exam_date:
            from django.utils import timezone
            delta = self.exam_date - timezone.now().date()
            return max(delta.days, 0)
        return None
