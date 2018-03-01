from django.conf.urls import url

from . import views	

urlpatterns = [
    url(r"^posts/$", views.posts, name="get_posts")
]