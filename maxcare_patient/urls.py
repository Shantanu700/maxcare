from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path("register/", views.patient_registration, name="register"),
    path("register_doctor/", views.doctor_registration, name="doctor register"),
    path("signin/", views.signin, name="sign in"),
    path("logout/", views.signout, name="logout"),
    path("info/", views.info, name="info"),
    path("side_panel/", views.side_panel, name="side"),
    path("book_appointments/", views.manage_appointments, name="manage appointments"),
    path("manage_prescriptions/", views.manage_prescription, name="manage prescription"),
    path("analytics/", views.get_data, name="analytics"),
    path("test/", views.test, name="test"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)