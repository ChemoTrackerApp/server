from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class PatientProfile(models.Model):
    user = models.OneToOneField(User, to_field='id', primary_key=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = _("patient profile")
        verbose_name_plural = _("patient profiles")

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def as_dict(self):
        return {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.first_name,
            "firstName": self.user.email
        }

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        PatientProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    instance.patientprofile.save()