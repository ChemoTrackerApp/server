from django.conf.urls import url

from . import views	

urlpatterns = [
    url(r"^search/", views.users, name="users"),
    url(r"^profile/$", views.profile, name="profile"),
    url(r"^s3-info/", views.get_s3_info, name="s3-info")
]