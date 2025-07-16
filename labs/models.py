

# Create your models here.
# models.py

from django.db import models
from django.contrib.auth.models import User

class LabTestRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    patient = models.ForeignKey(User, related_name='lab_test_requests', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='lab_test_requests_sent', on_delete=models.CASCADE)
    technician = models.ForeignKey(
        User,
        related_name='lab_test_requests_assigned',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    symptoms = models.TextField(blank=True, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)  # Doctor's notes if any

    def __str__(self):
        return f"Lab Test Request for {self.patient.username} by {self.doctor.username}"

class LabTestResult(models.Model):
    test_request = models.OneToOneField(LabTestRequest, related_name='result', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    result_file = models.FileField(upload_to='lab_results/', blank=True, null=True)
    result_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Lab Result for {self.test_request.patient.username}"
