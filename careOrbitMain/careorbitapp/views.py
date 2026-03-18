from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from datetime import datetime,date
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Appointment,  Visit, TestResult, DoctorNote, Record, Medication


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.passwordHash):
                request.session['user_id'] = user.userID
                return redirect('/dashboard/')
        except User.DoesNotExist:
            pass
        return render(request, 'careorbit/login.html', {'error': 'Incorrect email or password.'})
    return render(request, 'careorbit/login.html')



def logout(request):
    request.session.flush()
    return redirect('/login/')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        name = f"{first_name} {last_name}".strip()
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone', '')
        nhs = request.POST.get('nhsNumber', '')

        if password1 != password2:
            return render(request, 'careorbit/signup.html', {'error': 'Passwords do not match.'})

        if not name:
            return render(request, 'careorbit/signup.html', {'error': 'Name is required.'})

        user = User.objects.create(
            name=name,
            email=email,
            passwordHash=make_password(password1),
            nhsNumber=nhs,
            date_of_birth=dob,
            phoneNumber=phone,
            role='patient',
        )
        request.session['user_id'] = user.userID
        return redirect('/dashboard/')
    return render(request, 'careorbit/signup.html')

def forgot_password(request):
    return render(request, 'careorbit/forgot_password.html')

def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
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
    patient = get_current_patient()  # TODO: auth
    medications = Medication.objects.filter(patientID=patient)
    return render(request, "careorbit/refill.html", {"medications": medications})

def medication_report(request):#TODO: auth
    patient = get_current_patient()

    medications = Medication.objects.filter(patientID=patient)

    context = {
        "patient": patient,
        "medications": medications,
    }

    return render(request, "careorbit/report.html", context)

def appointments(request):
    return render(request, "careorbit/Appointments.html")

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
    return render(request, "careorbit/private-policy.html")

def terms_of_service(request):
    return render(request, "careorbit/terms_of_service.html")

def contact_us(request):
    return render(request, "careorbit/contact_us.html")

def get_current_patient():#TODO: after authentication is implemented, this function should return the currently logged in patient
    return User.objects.filter(role='patient').first()

def appointment_data(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'No one is logged in.'}, status=401)
        
    # make sure user exists within DB
    try:
        user = User.objects.get(userID=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usr doesnt exist in db.'}, status=404)

    # Get appointments
    today = date.today()
    upcoming_appointments = Appointment.objects.filter(
        patientID=user,
        appointmentDate__gte=today
    ).order_by('appointmentDate', 'appointmentTime')

    appointments_list = []
    for appt in upcoming_appointments:
        appointments_list.append({
            'doctor_name': appt.doctorID.name if appt.doctorID else 'Unknown Doctor',
            'reason': appt.appointmentReason,

            'date': appt.appointmentDate.strftime('%Y-%m-%d'), 
            'time': appt.appointmentTime.strftime('%H:%M') if appt.appointmentTime else '', 
            'status': appt.status
        })


    return JsonResponse({'appointments': appointments_list})

def update_data(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'No one is logged in.'}, status=401)

    # make sure user exists within DB
    try:
        user = User.objects.get(userID=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'usr doesnt exist in db.'}, status=404)

    # Get medications that need a refill
    refill_medications = Medication.objects.filter(
        patientID=user,
        needsRefill=True
    )

    medications_list = []
    for med in refill_medications:
        medications_list.append({
            'name': med.name,
            'dosage': med.dosage,
            'frequency': med.frequency,
        })

    return JsonResponse({'medications': medications_list})