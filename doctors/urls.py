from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard_view, name="doctor_dashboard"),
    path('lab/dashboard/', views.lab_dashboard, name='lab_dashboard'),         # lab technician dashboard
    
    path('lab/result/<int:test_request_id>/', views.view_lab_result, name='view_lab_result'), 
]
