from django.urls import path
from . import views




urlpatterns = [

    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("logout/", views.logout, name="logout"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("records/", views.records, name="records"),
    path("records/test-results/", views.test_results, name="test_results"),
    path("records/visit-history/", views.visit_history, name="visit_history"),
    path("records/doctors-notes/", views.doctors_notes, name="doctors_notes"),
    path("records/general-documents/", views.general_documents, name="general_documents"),

    path("medications/", views.medications, name="medications"),
    path("medications/refill/", views.medication_refill, name="medication_refill"),
    path("medications/report/", views.medication_report, name="medication_report"),

    path("appointments/", views.appointments, name="appointments"),
    path("appointments/book/", views.book_appointment, name="book_appointment"),

    path("dependents/", views.dependents, name="dependents"),

    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path("contact-us/", views.contact_us, name="contact_us"),
]