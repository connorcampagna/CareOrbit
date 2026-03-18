from django.contrib import admin
from .models import User, Appointment, Visit, TestResult, DoctorNote, Record, Medication,DoctorSchedule

# All List Displays Below Are Shown Within Admin When Record Hasnt Been Clicked on Within DB
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'nhsNumber')

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointmentID', 'patientID', 'doctorID', 'appointmentDate', 'status')

class VisitAdmin(admin.ModelAdmin):
    list_display = ('visitID', 'patientID', 'doctorID', 'visitDate', 'visitType')

class MedicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'patientID', 'dosage', 'needsRefill')

class RecordAdmin(admin.ModelAdmin):
    list_display = ('documentType', 'patientID', 'uploadedAt')

class TestResultAdmin(admin.ModelAdmin):
    list_display = ('testName', 'patientID', 'resultDate')



admin.site.register(User, UserAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(Medication, MedicationAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(TestResult,TestResultAdmin)
admin.site.register(DoctorNote)
admin.site.register(DoctorSchedule)

