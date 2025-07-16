# patients/models.py

from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    symptoms = models.TextField()
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
     # Pending, Approved, Rejected

    def __str__(self):
        return f"{self.patient.username} -> Dr. {self.doctor.user.username})"

class Diagnosis(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnoses')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diagnosis for {self.patient.username} by Dr. {self.doctor.user.username}"

class Prescription(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    file = models.FileField(upload_to='prescriptions/')
    text = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.username} by Dr. {self.doctor.user.username}"
