from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('lab technician', 'Lab Technician'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def save(self, *args, **kwargs):
        if self.role:
            self.role = self.role.lower()  # This ensures the role is always lowercase on save
        super().save(*args, **kwargs)