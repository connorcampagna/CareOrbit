from django.db import models
from django.core.exceptions import ValidationError


class User(models.Model):
    # User is Either Patient Or Doctor
    userRoles = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    
    #ALl User Fields 
    userID = models.AutoField(primary_key=True)
    parentID = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    passwordHash = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=userRoles)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=255)
    phoneNumber = models.CharField(max_length=20)
    nhsNumber = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return f"{self.name} : {self.role}, DOB : {self.date_of_birth} "

    def clean(self):
        # User cant be own parent
        if self.parentID and self.parentID.userID == self.userID:
            raise ValidationError("A user cannot be their own parent.")
        
        # Prevent a doctor from being set as a parent (Doctor would need to have seperate user account if they wanted to create a child)
        if self.parentID and self.parentID.role != 'patient':
            raise ValidationError("Only patients can be set as a parent (guardian).") 
    

class Appointment(models.Model):
    # All Appointment Status Types
    statusTypes = [
        ('booked', 'Booked'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    # All Appointment Types
    visitTypes = [('in_person', 'In Person'), ('virtual', 'Virtual')]

    # Appointment Fields
    appointmentID = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patientAppointments')
    doctorID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointmentReason = models.CharField(max_length=132)
    visitType = models.CharField(max_length=20, choices=visitTypes)
    appointmentDate = models.DateField()
    appointmentTime = models.TimeField(default='00:00:00')
    status = models.CharField(max_length=20, choices=statusTypes, default='booked')

    def clean(self):
        # Patient cant be doctor
        if self.doctorID and self.doctorID.role != 'doctor':
            raise ValidationError("Only doctors can be assigned as the doctor for an appointment.")
        # Doctor cannt get an appointment
        if self.patientID and self.patientID.role != 'patient':
            raise ValidationError("Only patients can have an appointment.")

    def __str__(self):
        return f"Appointment ID : {self.appointmentID}, Patient : {self.patientID}"


class Visit(models.Model):
    # All Visit Types
    visitTypes = [
        ('in_person', 'In Person'),
        ('virtual', 'Virtual'),
    ]

    #Visit Fields
    visitID = models.AutoField(primary_key=True)
    appointmentID = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    patientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patientVisits')
    doctorID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctorVisits')
    visitType = models.CharField(max_length=20, choices=visitTypes)
    summary = models.TextField()
    visitDate = models.DateTimeField()

    def __str__(self):
        return f"Visit ID : {self.visitID}, Patient : {self.patientID}"



#Test Result Fields
class TestResult(models.Model):
    testID = models.AutoField(primary_key=True)
    visitID = models.ForeignKey(Visit, on_delete=models.CASCADE)
    patientID = models.ForeignKey(User, on_delete=models.CASCADE)
    testName = models.CharField(max_length=255)
    result = models.TextField()
    resultDate = models.DateField()

    def __str__(self):
        return f"Test ID : {self.testName}, Patient : {self.patientID}"

#Doctors Note Fields 
class DoctorNote(models.Model):
    noteID = models.AutoField(primary_key=True)
    visitID = models.ForeignKey(Visit, on_delete=models.CASCADE)
    doctorID = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Doctor Note ID : {self.noteID}, Doctor : {self.doctorID}"


class Record(models.Model):
    # All Document Types
    documentTypes = [
        ('tests', 'Tests'),
        ('visitHistory', 'Visit History'),
        ('notes', 'Notes'),
        ('meds', 'Medications'),
        ('general', 'General'),
    ]

    #Record Fields 
    recordID = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(User, on_delete=models.CASCADE)
    visitID = models.ForeignKey(Visit, on_delete=models.SET_NULL, null=True, blank=True)
    documentType = models.CharField(max_length=20, choices=documentTypes)
    fileUrl = models.CharField(max_length=500)
    uploadedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Type of Records : {self.documentType}, Patient : {self.patientID}"



#All Medication Fields
class Medication(models.Model):
    medicationID = models.AutoField(primary_key=True)
    patientID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicationsReceived')
    doctorID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='medicationsPrescribed')
    name = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255)
    needsRefill = models.BooleanField(default=False)
    prescribedAt = models.DateField()

    def __str__(self):
        return f"Medication ID : {self.medicationID}, Medication : {self.name}, Patient : {self.patientID}"

class DoctorSchedule(models.Model):

    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    doctorID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    day = models.IntegerField(choices=DAYS_OF_WEEK)
    startTime = models.TimeField()
    endTime = models.TimeField()
    appointmentDuration = models.IntegerField(default=30) 

    def clean(self):
        # Patient cant be assigned a schedule
        if self.doctorID and self.doctorID.role != 'doctor':
            raise ValidationError("Only doctors can have a schedule.")

    class Meta:
        unique_together = ('doctorID', 'day') # only one schedule a day

    def __str__(self):
        return f"{self.doctorID.name} Schedule - {self.get_day_display()}"
