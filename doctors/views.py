from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from patients.models import Appointment, Diagnosis, Prescription
from doctors.models import Doctor
from labs.models import LabTestRequest, LabTestResult
from users.models import Profile
from django.db.models import Count
@login_required
def dashboard_view(request):
    # Check if logged-in user is a doctor
    if not (hasattr(request.user, 'profile') and request.user.profile.role == 'doctor'):
        return HttpResponseForbidden("You are not authorized to view this page.")

    doctor = get_object_or_404(Doctor, user=request.user)

    # Get all appointments for this doctor
    appointments = Appointment.objects.filter(doctor=doctor)

    # Lab test requests for this doctor
    doctor_lab_requests = LabTestRequest.objects.filter(doctor=request.user).order_by('-requested_at')

    # Initialize context variables
    selected_patient = None
    previous_diagnoses = []
    previous_prescriptions = []
    upload_success = False
    diagnosis_saved = False
    lab_test_requested = False

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "select_patient":
            selected_patient_id = request.POST.get("selected_patient")
            if selected_patient_id:
                selected_patient = get_object_or_404(User, id=selected_patient_id)
                previous_diagnoses = Diagnosis.objects.filter(patient=selected_patient)
                previous_prescriptions = Prescription.objects.filter(patient=selected_patient)

        elif action == "add_diagnosis":
            selected_patient_id = request.POST.get("selected_patient")
            if selected_patient_id:
                selected_patient = get_object_or_404(User, id=selected_patient_id)
                diagnosis_notes = request.POST.get("diagnosis_notes", "").strip()
                if diagnosis_notes:
                    Diagnosis.objects.create(
                        patient=selected_patient,
                        doctor=doctor,
                        notes=diagnosis_notes
                    )
                    diagnosis_saved = True
                previous_diagnoses = Diagnosis.objects.filter(patient=selected_patient)
                previous_prescriptions = Prescription.objects.filter(patient=selected_patient)

        elif action == "upload_prescription":
            selected_patient_id = request.POST.get("selected_patient")
            if selected_patient_id:
                selected_patient = get_object_or_404(User, id=selected_patient_id)

                file = request.FILES.get("prescription_file")
                typed_text = request.POST.get("typed_prescription", "").strip()

                if file or typed_text:
                    Prescription.objects.create(
                        patient=selected_patient,
                        doctor=doctor,
                        file=file if file else None,
                        text=typed_text if typed_text else ""
                    )
                    upload_success = True

                previous_diagnoses = Diagnosis.objects.filter(patient=selected_patient)
                previous_prescriptions = Prescription.objects.filter(patient=selected_patient)

        elif action == 'request_lab_test':
            patient_id = request.POST.get('selected_patient')
            notes = request.POST.get('lab_test_notes', '').strip()
            if patient_id:
                patient = get_object_or_404(User, id=patient_id)

                technicians = User.objects.filter(profile__role='lab_technician') \
                .annotate(workload=Count('lab_test_requests_assigned')) \
                .order_by('workload')

                print("Technicians found:", technicians)


                if technicians.exists():
                    assigned_technician = technicians.first()
                    print("Assigned technician:", assigned_technician)
                    LabTestRequest.objects.create(
                        patient=patient,
                        doctor=request.user,
                        technician=assigned_technician,
                        notes=notes
                    )
                lab_test_requested = True
                
                # Optionally refresh lab requests
                doctor_lab_requests = LabTestRequest.objects.filter(doctor=request.user).order_by('-requested_at')

    context = {
        "appointments": appointments,
        "selected_patient": selected_patient,
        "previous_diagnoses": previous_diagnoses,
        "previous_prescriptions": previous_prescriptions,
        "upload_success": upload_success,
        "diagnosis_saved": diagnosis_saved,
        "lab_test_requested": lab_test_requested,
        "doctor_lab_requests": doctor_lab_requests,
        "all_patients": User.objects.filter(profile__role='patient'),
    }
    return render(request, "doctors/doctor_dashboard.html", context)


@login_required
def lab_dashboard(request):
    profile = request.user.profile
    print(f"User: {request.user}, Role: {repr(profile.role)}")
    
    if profile.role.lower() != 'lab technician':
     return HttpResponseForbidden("You do not have permission to access this page.")


    pending_lab_requests = LabTestRequest.objects.filter(
        technician=request.user,
        status='pending'
    ).order_by('requested_at')
    completed_lab_results = LabTestResult.objects.select_related('test_request').order_by('-uploaded_at')

    if request.method == "POST":
        action = request.POST.get('action')

        if action == 'upload_lab_result':
            test_request_id = request.POST.get('test_request_id')
            test_request = get_object_or_404(LabTestRequest, id=test_request_id,technician=request.user)
            result_text = request.POST.get('result_text', '').strip()
            result_file = request.FILES.get('result_file', None)

            if test_request.technician != request.user:
             return HttpResponseForbidden("You are not authorized to upload this result.")


            lab_result, created = LabTestResult.objects.get_or_create(test_request=test_request)
            if result_text:
                lab_result.result_text = result_text
            if result_file:
                lab_result.result_file = result_file
            lab_result.save()

            test_request.status = 'completed'
            test_request.save()

            return redirect('lab_dashboard')

    context = {
        'pending_lab_requests': pending_lab_requests,
        'completed_lab_results': completed_lab_results,
    }
    return render(request, 'labs/lab_dashboard.html', context)





@login_required
def view_lab_result(request, test_request_id):
    test_request = get_object_or_404(LabTestRequest, id=test_request_id)

    user_profile = getattr(request.user, 'profile', None)
    if not user_profile:
        return HttpResponseForbidden("Not authorized")

    if (user_profile.role == 'patient' and test_request.patient != request.user) or \
       (user_profile.role == 'doctor' and test_request.doctor != request.user) and \
       user_profile.role != 'lab technician':
        return HttpResponseForbidden("Not authorized")

    try:
        lab_result = test_request.result
    except LabTestResult.DoesNotExist:
        lab_result = None

    message = None
    if not lab_result:
        message = "No results uploaded yet."

    context = {
        'test_request': test_request,
        'lab_result': lab_result,
        'message': message,
    }

    return render(request, 'labs/view_lab_result.html', context)

