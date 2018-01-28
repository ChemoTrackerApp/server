from django.conf.urls import url

from . import views	

urlpatterns = [
    url(r"", views.users, name="users"),
    url(r"profile", views.profile, name="profile")
]