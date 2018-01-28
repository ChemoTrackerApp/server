from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class PatientProfile(models.Model):
    user = models.OneToOneField(User, to_field='id', primary_key=True)

    class Meta:
        verbose_name = _("patient profile")
        verbose_name_plural = _("patient profiles")

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def as_dict(self):
        return {
            "id": self.user.id,
            "firstName": self.user.first_name,
            "lastName": self.user.last_name,
            "email": self.user.email
        }

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        PatientProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    instance.patientprofile.save()