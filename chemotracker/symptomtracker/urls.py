from django.conf.urls import url

from . import views	

urlpatterns = [
    url(r"^symptoms/$", views.symptoms, name="get_symptoms"),
    url(r"grades", views.grades, name="get_grades")
]