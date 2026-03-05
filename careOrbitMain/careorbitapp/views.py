from django.shortcuts import render
from django.http import HttpResponse


def login(request):
    return HttpResponse("Login page")

def signup(request):
    return HttpResponse("Signup page")

def forgot_password(request):
    return HttpResponse("Forgot password page")

def dashboard(request):
    return HttpResponse("Dashboard")

def records(request):
    return HttpResponse("Records")

def test_results(request):
    return HttpResponse("Test Results")

def visit_history(request):
    return HttpResponse("Visit History")

def doctors_notes(request):
    return HttpResponse("Doctor Notes")

def general_documents(request):
    return HttpResponse("General Documents")

def medications(request):
    return HttpResponse("Medications")

def medication_refill(request):
    return HttpResponse("Medication Refill")

def medication_report(request):
    return HttpResponse("Report Medication")

def appointments(request):
    return HttpResponse("Appointments")

def book_appointment(request):
    return HttpResponse("Book Appointment")

def dependents(request):
    return HttpResponse("Dependents")

def privacy_policy(request):
    return HttpResponse("Privacy Policy")

def terms_of_service(request):
    return HttpResponse("Terms of Service")

def contact_us(request):
    return HttpResponse("Contact Us")
