from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from doctors.models import Doctor # Ensure these are defined in your models.py


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect superuser to admin dashboard
            else:
                return redirect('dashboard')        # Redirect based on user role
        else:
            messages.error(request, "Invalid credentials")
            return render(request, "users/login.html")
    return render(request, "users/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        role = request.POST.get("role", "").strip()

        # Doctor-specific fields
        specialty = request.POST.get("specialty", "").strip()
        experience = request.POST.get("experience", "").strip()

        if not username or not email or not password or not role:
            messages.error(request, "All fields including role are required.")
            return render(request, "users/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "users/register.html")

        user = User.objects.create_user(username=username, email=email, password=password)
        profile, created = Profile.objects.get_or_create(user=user, defaults={'role': role})
        if not created:
         profile.role = role
         profile.save()

        if role == "Doctor":
            Doctor.objects.create(
                user=user,
                specialty=specialty,
                experience_years=int(experience) if experience.isdigit() else 0
            )

        messages.success(request, "Registered successfully. You can now log in.")
        return redirect('login')

    return render(request, "users/register.html")


def dashboard_view(request):
    if request.user.is_superuser:
        return render(request, "users/admin_dashboard.html")  # For superuser

    role = request.user.profile.role.lower()

    if role == "doctor":
        return redirect("doctor_dashboard")
    elif role == "patient":
        return redirect("patient_dashboard")
    elif role == "lab technician":
        return redirect("lab_dashboard")
    else:
        messages.error(request, "Invalid user role.")
        return redirect('login')


def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('dashboard')
    return render(request, "users/admin_dashboard.html")

