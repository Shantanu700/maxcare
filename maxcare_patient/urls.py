from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path("register/", views.patient_registration, name="register"),
    path("signin/", views.signin, name="sign in"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)