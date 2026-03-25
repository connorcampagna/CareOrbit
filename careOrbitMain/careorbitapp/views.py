import json
from django.http import JsonResponse
from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Appointment,  Visit, TestResult, DoctorNote, Record, Medication


# Login 
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        try:
            user = User.objects.get(email=email,parentID__isnull=True) # parent_ID is null as once you add depdent it returns 2 users
            if check_password(password, user.passwordHash):
                request.session['user_id'] = user.userID
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)

                return redirect('/dashboard/')
        except User.DoesNotExist:
            pass
        return render(request, 'careorbit/login.html', {'error': 'Incorrect email or password.'})
    return render(request, 'careorbit/login.html')


#Logout 
def logout(request):
    request.session.flush()
    return redirect('/login/')

#Sign up 
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

# Forgot password
def forgot_password(request):
    return render(request, 'careorbit/forgot_password.html')

#dashboard
def dashboard(request):
    if not request.session.get('user_id'):
        return redirect('/login/')
    
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')


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

#All Records (Visits, Tests, Documents, Doctors Notes)
def records(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    dependents = User.objects.filter(parentID=patient)

    view_for_id = request.GET.get('view_for')
    viewed_patient = patient
    if view_for_id:
        dep = dependents.filter(userID=view_for_id).first()
        if dep:
            viewed_patient = dep

    patient_visits = Visit.objects.filter(patientID=viewed_patient)
    recent_results = TestResult.objects.filter(
        patientID=viewed_patient
    ).order_by("-resultDate")[:5]

    recent_notes = DoctorNote.objects.filter(
        visitID__in=patient_visits
    ).order_by("-createdAt")[:5]

    recent_documents = Record.objects.filter(
        patientID=viewed_patient
    ).order_by("-uploadedAt")[:5]

    recent_visits = patient_visits.order_by("-visitDate")[:5]

    context = {
        "patient": patient,
        "dependents": dependents,
        "recent_results": recent_results,
        "recent_notes": recent_notes,
        "recent_documents": recent_documents,
        "recent_visits": recent_visits,
    }

    return render(request, "careorbit/records.html", context)

# Test Results
def test_results(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')


    results = TestResult.objects.filter(
        patientID=patient
    ).order_by('-resultDate')

    context = {
        "patient": patient,
        "results": results,
    }

    return render(request, "careorbit/test_results.html", context)

#Vists 
def visit_history(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    visits = Visit.objects.filter(patientID=patient).order_by("-visitDate")

    context = {
        "patient": patient,
        "visits": visits,
    }

    return render(request, "careorbit/visit_history.html", context)

#Doctors Notes
def doctors_notes(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')


    patient_visits = Visit.objects.filter(patientID=patient)
    notes = DoctorNote.objects.filter(visitID__in=patient_visits).order_by("-createdAt")

    context = {
        "patient": patient,
        "notes": notes,
    }

    return render(request, "careorbit/doctors_notes.html", context)

#Documents
def general_documents(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')


    documents = Record.objects.filter(
        patientID=patient,
        documentType="general"
    ).order_by("-uploadedAt")

    context = {
        "patient": patient,
        "documents": documents,
    }

    return render(request, "careorbit/general_documents.html", context)

# All Medication Views
def medications(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    dependents = User.objects.filter(parentID=patient)

    view_for_id = request.GET.get('view_for')
    viewed_patient = patient
    if view_for_id:
        dep = dependents.filter(userID=view_for_id).first()
        if dep:
            viewed_patient = dep

    meds = Medication.objects.filter(patientID=viewed_patient).order_by("-prescribedAt")
    refill_needed = meds.filter(needsRefill=True)

    context = {
        "patient": patient,
        "viewed_patient": viewed_patient,
        "dependents": dependents,
        "medications": meds,
        "refill_needed": refill_needed,
    }

    return render(request, "careorbit/medications.html", context)

# refill 
def medication_refill(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    dependents = User.objects.filter(parentID=patient)

    view_for_id = request.GET.get('view_for') or request.POST.get('view_for')
    viewed_patient = patient
    if view_for_id:
        dep = dependents.filter(userID=view_for_id).first()
        if dep:
            viewed_patient = dep

    success = False
    if request.method == 'POST':
        med_name = request.POST.get('medication')
        if med_name:
            Medication.objects.filter(patientID=viewed_patient, name=med_name).update(needsRefill=True)
            success = True

    medications = Medication.objects.filter(patientID=viewed_patient)

    context = {
        "patient": patient,
        "viewed_patient": viewed_patient,
        "dependents": dependents,
        "medications": medications,
        "success": success,
    }
    return render(request, "careorbit/refill.html", context)

# report 
def medication_report(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    dependents = User.objects.filter(parentID=patient)

    view_for_id = request.GET.get('view_for') or request.POST.get('view_for')
    viewed_patient = patient
    if view_for_id:
        dep = dependents.filter(userID=view_for_id).first()
        if dep:
            viewed_patient = dep

    success = False
    if request.method == 'POST':
        med_name = request.POST.get('medication')
        symptom = request.POST.get('symptom')
        severity = request.POST.get('severity')
        started_date = request.POST.get('started_date')
        if med_name and symptom and severity and started_date:
            success = True

    medications = Medication.objects.filter(patientID=viewed_patient)

    context = {
        "patient": patient,
        "viewed_patient": viewed_patient,
        "dependents": dependents,
        "medications": medications,
        "success": success,
    }

    return render(request, "careorbit/report.html", context)

# All appointment views
def appointments(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    dependents = User.objects.filter(parentID=patient)

    view_for_id = request.GET.get('view_for')
    viewed_patient = patient
    if view_for_id:
        dep = dependents.filter(userID=view_for_id).first()
        if dep:
            viewed_patient = dep

    upcoming = Appointment.objects.filter(
        patientID=viewed_patient,
        appointmentDate__gte=date.today(),
        status='booked'
    ).order_by('appointmentDate', 'appointmentTime')

    appointments_list = []
    for appt in upcoming:
        appointments_list.append({
            "id": appt.appointmentID,
            "appointmentReason": appt.appointmentReason,
            "appointmentDate": appt.appointmentDate,
            "appointmentTime": appt.appointmentTime,
            "doctorID": appt.doctorID,
            "visitType": appt.visitType,
            "get_visitType_display": "Virtual" if appt.visitType == 'virtual' else "In-Person",
        })

    context = {
        "patient": patient,
        "dependents": dependents, 
        "appointments": appointments_list,
    }
    return render(request, "careorbit/appointments.html", context)


def cancel_appointment(request):
    if request.method == 'POST':
        patient = get_current_patient(request)
        try:
            data = json.loads(request.body)
            appt_id = data.get('appointment_id')
            appt = Appointment.objects.get(appointmentID=appt_id, patientID=patient)
            appt.delete()
            return JsonResponse({'status': 'success'})
        except Appointment.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment doesnt exist'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def book_appointment(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    doctors = User.objects.filter(role='doctor')
    
    dependents = User.objects.filter(parentID=patient)
    
    context = {
        "patient": patient,
        "dependents": dependents,
        "doctors": doctors,
    }

    if request.method == 'POST':
        selected_patient_id = request.POST.get('patient_id')
        booked_for_patient = patient 
        
        if selected_patient_id and selected_patient_id != 'self':
            dep = dependents.filter(userID=selected_patient_id).first()
            if dep:
                booked_for_patient = dep

        reason = request.POST.get('reason')
        other_description = request.POST.get('other_description')
        visit_type = request.POST.get('visit_type')
        preferred_date = request.POST.get('date')
        doctor_id = request.POST.get('doctor')
        selected_slot = request.POST.get('selected_slot')
        
        if not preferred_date:
            context["error"] = "Please select a date."
            return render(request, "careorbit/book_appointment.html", context)

        if not selected_slot:
            context["error"] = "Please select a time slot."
            return render(request, "careorbit/book_appointment.html", context)

        if not visit_type:
            context["error"] = "Please select visit type."
            return render(request, "careorbit/book_appointment.html", context)

        if not doctor_id:
            context["error"] = "Please select a doctor."
            return render(request, "careorbit/book_appointment.html", context)
        
        if reason == 'other':
            if not other_description:
                context["error"] = "Please describe your reason."
                return render(request, "careorbit/book_appointment.html", context)
            appointment_reason = other_description
        else:
            appointment_reason = reason
        
        try:
            selected_doctor = User.objects.get(userID=doctor_id, role='doctor')
        except User.DoesNotExist:
            context["error"] = "Invalid doctor."
            return render(request, "careorbit/book_appointment.html", context)
        
        Appointment.objects.create(
            patientID=booked_for_patient, 
            doctorID=selected_doctor,
            appointmentReason=appointment_reason,
            visitType=visit_type,
            appointmentDate=preferred_date,
            appointmentTime=selected_slot,
            status='booked'
        )

        context["success"] = "Appointment booked successfully"
        return render(request, "careorbit/book_appointment.html", context)

    return render(request, "careorbit/book_appointment.html", context)


def get_available_slots(request):
    selected_date = request.GET.get('date')
    doctor_id = request.GET.get('doctor')

    if not selected_date:
        return JsonResponse({'booked_slots': []})

    filters = {'appointmentDate': selected_date}
    if doctor_id:
        filters['doctorID'] = doctor_id

    booked = Appointment.objects.filter(**filters).values_list('appointmentTime', flat=True)
    booked_slots = [t.strftime('%H:%M') for t in booked if t]

    return JsonResponse({'booked_slots': booked_slots})

# All appointment 
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

# Footer Views

def privacy_policy(request):
    return render(request, "careorbit/private-policy.html")

def terms_of_service(request):
    return render(request, "careorbit/terms_of_service.html")

def contact_us(request):
    return render(request, "careorbit/contact_us.html")



# Main Getter 
def get_current_patient(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    return User.objects.filter(userID=user_id).first()


# all related dependent views

def dependents(request):
    user_id = request.session.get('user_id')
    patient = User.objects.filter(userID=user_id).first()

    dependents_qs = User.objects.filter(parentID=patient)
    dependents = []
    
    for dep in dependents_qs:
        badges = []
        
        # Check medications for refills needed
        if Medication.objects.filter(patientID=dep, needsRefill=True).exists():
            badges.append({'text': 'REFILL NEEDED', 'class': 'border border-warning text-warning fw-bold small px-2 py-1 rounded bg-white'})
            
        # Check upcoming appointments
        today = date.today()
        upcoming = Appointment.objects.filter(patientID=dep, appointmentDate__gte=today).order_by('appointmentDate').first()
        
        if upcoming:
            if upcoming.status == 'booked':
                badges.append({'text': 'APPOINTMENT CONFIRMED', 'class': 'border border-success text-success fw-bold small px-2 py-1 rounded bg-white'})
            elif upcoming.status == 'pending':
                badges.append({'text': 'CHECKUP DUE', 'class': 'border border-primary text-primary fw-bold small px-2 py-1 rounded bg-white'})
        else:
            badges.append({'text': 'NO UPCOMING APPOINTMENTS', 'class': 'border border-secondary text-secondary fw-bold small px-2 py-1 rounded bg-white'})
             
        dependents.append({
            'userID': dep.userID,
            'name': dep.name,
            'date_of_birth': dep.date_of_birth,
            'nhsNumber': dep.nhsNumber if dep.nhsNumber else 'N/A',
            'badges': badges
        })

    context = {
        "patient": patient,
        "dependents": dependents,
    }

    return render(request, "careorbit/dependents.html", context)

def add_dependent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            parent = User.objects.get(userID=request.session.get('user_id'))
            
            nhs_val = data.get('nhs', '').strip()
            if not nhs_val:
                nhs_val = None
                
            # dependent 
            dependent = User.objects.create(
                parentID=parent, 
                role='patient',
                name=data.get('name'),
                date_of_birth=data.get('dob'),
                email=data.get('email'),
                phoneNumber=data.get('phone', ''),
                passwordHash='auto', 
                nhsNumber=  nhs_val
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Dependent added',
                'dependent_name': dependent.name,
                'nhs_number': dependent.nhsNumber
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def edit_dependent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dependent_id = data.get('dependent_id')
            
            dependent = User.objects.filter(userID=dependent_id).first()

            name = data.get('name', '').strip()
            dob = data.get('dob')
            nhs = data.get('nhs', '').strip()
            
            if name:
                dependent.name = name
            if dob:
                dependent.date_of_birth = dob
            if nhs:
                dependent.nhsNumber = nhs
            else:
                dependent.nhsNumber = None
                
            dependent.save()
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Profile updated',
                'name': dependent.name,
                'dob': dependent.date_of_birth.strftime('%Y-%m-%d') if dependent.date_of_birth else '',
                'nhs': dependent.nhsNumber or ''
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
 


def get_dependent_details(request):
    if request.method == 'GET':
        try:
            dependent_id = request.GET.get('id')
            dependent = User.objects.filter(userID=dependent_id).first()
            
            if not dependent:
                return JsonResponse({'status': 'error', 'message': 'Dependent not found.'}, status=404)

            
            today = date.today()
            upcomingAppointments = Appointment.objects.filter(
                patientID=dependent,
                appointmentDate__gte=today
            ).order_by('appointmentDate', 'appointmentTime')
            
            # all appoinments for dependent 
            appointments_list = []
            for appt in upcomingAppointments:
                appointments_list.append({
                    'doctor': appt.doctorID.name if appt.doctorID else 'Unknown Provider',
                    'reason': appt.appointmentReason,
                    'date': appt.appointmentDate.strftime('%b %d, %Y'),
                    'time': appt.appointmentTime.strftime('%I:%M %p') if appt.appointmentTime else '',
                    'status': appt.status.upper()
                })
                
            # all active medication for dependent 
            medications = Medication.objects.filter(patientID=dependent).order_by('-prescribedAt')
            medications_list = []
            for med in medications:
                medications_list.append({
                    'name': med.name,
                    'dosage': med.dosage,
                    'frequency': med.frequency,
                    'doctor': med.doctorID.name if med.doctorID else 'Unknown Provider',
                    'needs_refill': med.needsRefill
                })
                
            return JsonResponse({
                'status': 'success',
                'appointments': appointments_list,
                'medications': medications_list
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



def delete_dependent(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            dependent_id = data.get('dependent_id')
            
            dependent = User.objects.filter(userID=dependent_id).first()
            dependent.delete()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def profile(request):
    patient = get_current_patient(request)
    if not patient:
        return redirect('/login/')

    context = {
        "patient": patient
    }

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        dob = request.POST.get('dob')
        phone = request.POST.get('phone', '').strip()
        nhs = request.POST.get('nhs', '').strip()

        if name:
            patient.name = name
        if dob:
            patient.date_of_birth = dob
        patient.phoneNumber = phone
        patient.nhsNumber = nhs if nhs else None
        patient.save()
        context["success"] = "Profile updated successfully!"
    return render(request, "careorbit/profile.html", context)
 