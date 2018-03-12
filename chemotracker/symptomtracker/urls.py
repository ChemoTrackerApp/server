from django.conf.urls import url

from . import views	

urlpatterns = [
    url(r"^symptoms/$", views.symptoms, name="get_symptoms"),
    url(r"grades", views.grades, name="get_grades"),
    url(r"patientsymptoms", views.get_patient_symptoms, name="get_patient_symptoms"),
    url(r"interventions", views.get_interventions, name="get_interventions"),
    url(r"streak", views.streak, name="streak"),
]