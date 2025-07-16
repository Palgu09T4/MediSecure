from django.urls import path
from doctors.views import lab_dashboard

urlpatterns = [
    path('dashboard/', lab_dashboard, name='lab_dashboard'),
]
