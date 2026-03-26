import os
import sys
import django
from datetime import date, time, datetime


sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'careOrbitConfigs.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from careorbitapp.models import (
    User, Appointment, Visit, Medication, Record, DoctorNote, TestResult
)


def clear_data():
    print("Clearing existing data...")
    TestResult.objects.all().delete()
    DoctorNote.objects.all().delete()
    Record.objects.all().delete()
    Medication.objects.all().delete()
    Visit.objects.all().delete()
    Appointment.objects.all().delete()
    User.objects.all().delete()
    print("Done.\n")


def populate():
    clear_data()

    print("Creating doctors...")

    dr_smith = User.objects.create(
        role='doctor',
        name='Dr. Sarah Smith',
        date_of_birth=date(1975, 4, 12),
        email='sarah.smith@careorbit.nhs.uk',
        phoneNumber='07700900001',
        passwordHash=make_password('hashed_password'),
        nhsNumber=None
    )

    dr_patel = User.objects.create(
        role='doctor',
        name='Dr. Raj Patel',
        date_of_birth=date(1980, 8, 23),
        email='raj.patel@careorbit.nhs.uk',
        phoneNumber='07700900002',
        passwordHash=make_password('hashed_password'),
        nhsNumber=None
    )

    dr_jones = User.objects.create(
        role='doctor',
        name='Dr. Emily Jones',
        date_of_birth=date(1985, 2, 17),
        email='emily.jones@careorbit.nhs.uk',
        phoneNumber='07700900003',
        passwordHash=make_password('hashed_password'),
        nhsNumber=None
    )

    print("Creating patients...")

    alice = User.objects.create(
        role='patient',
        name='Alice Johnson',
        date_of_birth=date(1990, 6, 15),
        email='testpatient@gmail.com',
        phoneNumber='07700900010',
        passwordHash=make_password('password123'),
        nhsNumber='111 222 3333'
    )

    bob = User.objects.create(
        role='patient',
        name='Bob Williams',
        date_of_birth=date(1985, 3, 22),
        email='bob.williams@email.com',
        phoneNumber='07700900011',
        passwordHash=make_password('password123'),
        nhsNumber='444 555 6666'
    )

    carol = User.objects.create(
        role='patient',
        name='Carol Davies',
        date_of_birth=date(1972, 11, 5),
        email='carol.davies@email.com',
        phoneNumber='07700900012',
        passwordHash=make_password('password123'),
        nhsNumber='777 888 9999'
    )

    print("Creating dependents (children)...")

    # Two dependents linked to Alice
    child1 = User.objects.create(
        role='patient',
        name='Sam Johnson',
        date_of_birth=date(2015, 7, 10),
        email='sam.johnson.child@careorbit.nhs.uk',
        phoneNumber='',
        passwordHash=make_password('childpass123'),
        nhsNumber='100 200 3001',
        parentID=alice
    )

    child2 = User.objects.create(
        role='patient',
        name='Lily Johnson',
        date_of_birth=date(2018, 2, 28),
        email='lily.johnson.child@careorbit.nhs.uk',
        phoneNumber='',
        passwordHash=make_password('childpass123'),
        nhsNumber='100 200 3002',
        parentID=alice
    )

    # One dependent linked to Bob
    child3 = User.objects.create(
        role='patient',
        name='Jake Williams',
        date_of_birth=date(2012, 9, 3),
        email='jake.williams.child@careorbit.nhs.uk',
        phoneNumber='',
        passwordHash=make_password('childpass123'),
        nhsNumber='100 200 3003',
        parentID=bob
    )

    print("Creating appointments...")

    # Past appointments
    appt1 = Appointment.objects.create(
        patientID=alice,
        doctorID=dr_smith,
        appointmentReason='Annual health check',
        visitType='in_person',
        appointmentDate=date(2025, 10, 5),
        appointmentTime=time(9, 30),
        status='completed'
    )

    appt2 = Appointment.objects.create(
        patientID=alice,
        doctorID=dr_patel,
        appointmentReason='Blood pressure follow-up',
        visitType='virtual',
        appointmentDate=date(2025, 12, 12),
        appointmentTime=time(14, 0),
        status='completed'
    )

    # Upcoming appointments
    appt3 = Appointment.objects.create(
        patientID=alice,
        doctorID=dr_smith,
        appointmentReason='Routine checkup',
        visitType='in_person',
        appointmentDate=date(2026, 5, 20),
        appointmentTime=time(10, 0),
        status='booked'
    )

    appt4 = Appointment.objects.create(
        patientID=bob,
        doctorID=dr_jones,
        appointmentReason='Knee pain assessment',
        visitType='in_person',
        appointmentDate=date(2026, 4, 14),
        appointmentTime=time(11, 30),
        status='booked'
    )

    # Appointments for dependents
    appt5 = Appointment.objects.create(
        patientID=child1,
        doctorID=dr_patel,
        appointmentReason='Child vaccination',
        visitType='in_person',
        appointmentDate=date(2026, 4, 22),
        appointmentTime=time(9, 0),
        status='booked'
    )

    appt6 = Appointment.objects.create(
        patientID=child2,
        doctorID=dr_smith,
        appointmentReason='Growth check',
        visitType='in_person',
        appointmentDate=date(2026, 5, 1),
        appointmentTime=time(10, 30),
        status='booked'
    )

    print("Creating visits (past appointments with summaries)...")

    visit1 = Visit.objects.create(
        appointmentID=appt1,
        patientID=alice,
        doctorID=dr_smith,
        visitType='in_person',
        summary='Patient is in good health overall. Blood pressure slightly elevated. Advised to reduce salt intake and return in 3 months.',
        visitDate=datetime(2025, 10, 5, 9, 30)
    )

    visit2 = Visit.objects.create(
        appointmentID=appt2,
        patientID=alice,
        doctorID=dr_patel,
        visitType='virtual',
        summary='Follow-up on blood pressure. Readings have improved. Medication dosage adjusted.',
        visitDate=datetime(2025, 12, 12, 14, 0)
    )

    print("Creating doctor notes...")

    DoctorNote.objects.create(
        visitID=visit1,
        doctorID=dr_smith,
        content='Patient advised to monitor BP daily. Lifestyle changes recommended. Referred to nutritionist.'
    )

    DoctorNote.objects.create(
        visitID=visit2,
        doctorID=dr_patel,
        content='BP readings within acceptable range after lifestyle modifications. Continue current medication.'
    )

    print("Creating test results...")

    TestResult.objects.create(
        visitID=visit1,
        patientID=alice,
        testName='Full Blood Count (FBC)',
        result='All values within normal range. Haemoglobin 13.5 g/dL.',
        resultDate=date(2025, 10, 7)
    )

    TestResult.objects.create(
        visitID=visit1,
        patientID=alice,
        testName='Blood Pressure',
        result='145/90 mmHg - slightly elevated.',
        resultDate=date(2025, 10, 5)
    )

    TestResult.objects.create(
        visitID=visit2,
        patientID=alice,
        testName='Blood Pressure',
        result='128/82 mmHg - improved.',
        resultDate=date(2025, 12, 12)
    )

    print("Creating medications...")

    Medication.objects.create(
        patientID=alice,
        doctorID=dr_patel,
        name='Amlodipine',
        frequency='Once daily',
        dosage='5mg',
        needsRefill=False,
        prescribedAt=date(2025, 12, 12)
    )

    Medication.objects.create(
        patientID=alice,
        doctorID=dr_smith,
        name='Atorvastatin',
        frequency='Once daily at night',
        dosage='20mg',
        needsRefill=True,
        prescribedAt=date(2025, 10, 5)
    )

    Medication.objects.create(
        patientID=bob,
        doctorID=dr_jones,
        name='Ibuprofen',
        frequency='Twice daily with food',
        dosage='400mg',
        needsRefill=False,
        prescribedAt=date(2025, 11, 20)
    )

    Medication.objects.create(
        patientID=child1,
        doctorID=dr_patel,
        name='Amoxicillin',
        frequency='Three times daily',
        dosage='250mg',
        needsRefill=True,
        prescribedAt=date(2026, 3, 1)
    )

    print("Creating records/documents...")

    Record.objects.create(
        patientID=alice,
        visitID=visit1,
        documentType='notes',
        fileUrl='#',
        uploadedAt=datetime(2025, 10, 5, 12, 0)
    )

    Record.objects.create(
        patientID=alice,
        visitID=visit2,
        documentType='general',
        fileUrl='#',
        uploadedAt=datetime(2025, 12, 12, 16, 0)
    )

    print("Use for username : testpatient@gmail.com and password : password123 :)")



if __name__ == '__main__':
    populate()
