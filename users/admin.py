from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from doctors.models import Doctor  # Import Doctor model
from patients.models import Appointment, Diagnosis, Prescription

# Inline admin to include Profile inside UserAdmin
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

# Custom UserAdmin to include Profile info
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'get_role')

    def get_role(self, obj):
        return obj.profile.role
    get_role.short_description = 'Role'

    # Simplified field layout (no first_name/last_name)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

# Unregister original User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'experience_years')
    search_fields = ('user__username', 'specialty')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'preferred_date', 'preferred_time')
    list_filter = ('doctor',)
    search_fields = ('patient__username', 'doctor__user__username')

@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'created_at')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'uploaded_at')
