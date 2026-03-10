
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import render, redirect
from .models import User, Appointment,  Visit, TestResult, DoctorNote, Record, Medication


def login(request):
    return HttpResponse("Login page")

def signup(request):
    return HttpResponse("Signup page")

def forgot_password(request):
    return HttpResponse("Forgot password page")

def dashboard(request):
    patient = get_current_patient()#TODO: auth

    recent_medications = Medication.objects.filter(patientID=patient).order_by("-prescribedAt")[:3]
    recent_results = TestResult.objects.filter(patientID=patient).order_by("-resultDate")[:3]
    recent_visits = Visit.objects.filter(patientID=patient).order_by("-visitDate")[:3]
    dependents_count = User.objects.filter(parentID=patient).count()

    context = {
        "patient": patient,
        "recent_medications": recent_medications,
        "recent_results": recent_results,
        "recent_visits": recent_visits,
        "dependents_count": dependents_count,
    }

    return render(request, "careorbit/dashboard.html", context)

def records(request):
    patient = get_current_patient()#TODO: auth

    patient_visits = Visit.objects.filter(patientID=patient)
    recent_results = TestResult.objects.filter(
        patientID=patient
    ).order_by("-resultDate")[:5]

    recent_notes = DoctorNote.objects.filter(
        visitID__in=patient_visits
    ).order_by("-createdAt")[:5]

    recent_documents = Record.objects.filter(
        patientID=patient
    ).order_by("-uploadedAt")[:5]

    context = {
        "recent_results": recent_results,
        "recent_notes": recent_notes,
        "recent_documents": recent_documents,
    }

    return render(request, "careorbit/records.html", context)

def test_results(request):
    return HttpResponse("Test Results")

def visit_history(request):#TODO: auth
    patient = get_current_patient()

    visits = Visit.objects.filter(patientID=patient).order_by("-visitDate")

    context = {
        "patient": patient,
        "visits": visits,
    }

    return render(request, "careorbit/visit_history.html", context)

def doctors_notes(request):#TODO: auth
    patient = get_current_patient()

    patient_visits = Visit.objects.filter(patientID=patient)
    notes = DoctorNote.objects.filter(visitID__in=patient_visits).order_by("-createdAt")

    context = {
        "patient": patient,
        "notes": notes,
    }

    return render(request, "careorbit/doctors_notes.html", context)

def general_documents(request):#TODO: auth
    patient = get_current_patient()

    documents = Record.objects.filter(
        patientID=patient,
        documentType="general"
    ).order_by("-uploadedAt")

    context = {
        "patient": patient,
        "documents": documents,
    }

    return render(request, "careorbit/general_documents.html", context)

def medications(request):
    patient = get_current_patient()#TODO: auth 

    meds = Medication.objects.filter(patientID=patient).order_by("-prescribedAt")
    refill_needed = meds.filter(needsRefill=True)

    context = {
        "patient": patient,
        "medications": meds,
        "refill_needed": refill_needed,
    }

    return render(request, "careorbit/medications.html", context)

def medication_refill(request):
    return HttpResponse("Medication Refill")

def medication_report(request):#TODO: auth
    patient = get_current_patient()

    medications = Medication.objects.filter(patientID=patient)

    context = {
        "patient": patient,
        "medications": medications,
    }

    return render(request, "careorbit/medication_report.html", context)

def appointments(request):
    return HttpResponse("Appointments")

def book_appointment(request):
    return render(request, "careorbit/book_appointment.html", context)

def dependents(request):
    patient = get_current_patient()#TODO: auth

    dependents = User.objects.filter(parentID=patient)

    context = {
        "patient": patient,
        "dependents": dependents,
    }

    return render(request, "careorbit/dependents.html", context)

def privacy_policy(request):
    return HttpResponse("Privacy Policy")

def terms_of_service(request):
    return HttpResponse("Terms of Service")

def contact_us(request):
    return HttpResponse("Contact Us")

def get_current_patient():#TODO: after authentication is implemented, this function should return the currently logged in patient
    return User.objects.filter(role='patient').first()