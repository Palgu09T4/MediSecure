#patient/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from doctors.models import Doctor
from django.contrib.auth.models import User
from patients.models import Appointment,Prescription
from django.db.models import Count
from labs.models import LabTestRequest, LabTestResult

# Mapping from symptoms to specialties
SYMPTOM_SPECIALTY_MAP = {
    "fever": "General Physician",
    "cough": "Pulmonologist",
    "headache": "Neurologist",
    "diabetes": "Endocrinologist",
    "chest pain": "Cardiologist",
    # Add more mappings as needed
}

@login_required

def dashboard(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'patient':
        return redirect('login')

    appointment_requested = False
    matched_specialty = None
    error = None
    assigned_doctor = None

    if request.method == "POST":
        symptoms = request.POST.get("symptoms", "").strip().lower()
        preferred_date = request.POST.get("preferred_date")
        preferred_time = request.POST.get("preferred_time")

        SYMPTOM_SPECIALTY_MAP = {
            "fever": "General Physician",
            "cough": "Pulmonologist",
            "headache": "Neurologist",
            "diabetes": "Endocrinologist",
            "chest pain": "Cardiologist",
        }

        for symptom, specialty in SYMPTOM_SPECIALTY_MAP.items():
            if symptom in symptoms:
                matched_specialty = specialty
                break

        if matched_specialty:
            matching_doctors = Doctor.objects.filter(specialty__iexact=matched_specialty)\
                .annotate(workload=Count('appointments')).order_by('workload')
            if matching_doctors.exists():
                assigned_doctor = matching_doctors.first()
                Appointment.objects.create(
                    patient=request.user,
                    doctor=assigned_doctor,
                    symptoms=symptoms,
                    preferred_date=preferred_date,
                    preferred_time=preferred_time
                )
                appointment_requested = True
            else:
                error = f"No doctors available for specialty: {matched_specialty}"
        else:
            error = "No matching specialty found for your symptoms."

    # Load lab & prescription data
    user_lab_requests = LabTestRequest.objects.filter(patient=request.user).order_by('-requested_at')
    lab_results = LabTestResult.objects.filter(test_request__patient=request.user).order_by('-uploaded_at')
    prescriptions = Prescription.objects.filter(patient=request.user).order_by('-uploaded_at')

    context = {
        'user_lab_requests': user_lab_requests,
        'lab_results': lab_results,
        'prescriptions': prescriptions,
        'appointment_requested': appointment_requested,
        'assigned_doctor': (
          assigned_doctor.user.get_full_name().strip() or assigned_doctor.user.username
          ) if assigned_doctor else None,

        'specialty': assigned_doctor.specialty if assigned_doctor else None,
        'error': error,
    }

    return render(request, 'patients/patient_dashboard.html', context)
