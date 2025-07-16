from django.db import models
from django.contrib.auth.models import User

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)

    def __str__(self):
        return self.user.get_full_name()
    def save(self, *args, **kwargs):
        if self.role:
            self.role = self.role.lower()  # This ensures the role is always lowercase on save
        super().save(*args, **kwargs)
