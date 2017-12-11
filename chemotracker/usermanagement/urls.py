from django.conf.urls import patterns, url, include
from rest_framework import routers
 
router = routers.DefaultRouter()
router.register(r'accounts', views.PatientUserView, 'list')
 
urlpatterns = patterns(
    '',
    url(r'^/', include(router.urls)),
)