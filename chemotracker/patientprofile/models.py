from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

class PatientProfile(models.Model):
    user = models.OneToOneField(User, to_field='id', primary_key=True)
    image = models.URLField(null=True)
    gender = models.CharField(max_length=30, null=True)
    date_of_birth = models.DateField(null=True)
    phone_number = models.CharField(max_length=30, null=True)
    medical_conditions = ArrayField(models.CharField(max_length=100), null=True)
    medication_list = ArrayField(models.CharField(max_length=100), null=True)
    cancer_diagnosis = models.CharField(max_length=50, null=True)
    chemotherapy = models.CharField(max_length=3, null=True)

    class Meta:
        verbose_name = _("patient profile")
        verbose_name_plural = _("patient profiles")

    def __str__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def as_dict(self):
        allergies = Allergy.objects.filter(patient_id=self)
        allergies_dict = [ obj.as_dict() for obj in allergies ]
        return {
            "id": self.user.id,
            "firstName": self.user.first_name,
            "lastName": self.user.last_name,
            "image": self.image,
            "gender": self.gender,
            "dateOfBirth": self.date_of_birth.strftime('%Y-%m-%d'),
            "phoneNumber": self.phone_number,
            "emailAddress": self.user.email,
            "allergy": allergies_dict,
            "medicalConditions": self.medical_conditions,
            "medicationList": self.medication_list,
            "cancerDiagnosis": self.cancer_diagnosis,
            "chemotherapy": self.chemotherapy
        }

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        PatientProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_patient_profile(sender, instance, **kwargs):
    instance.patientprofile.save()


class Allergy (models.Model):
    patient = models.ForeignKey('PatientProfile', on_delete=models.CASCADE)
    allergen = models.CharField(max_length=30)
    reaction = ArrayField(models.CharField(max_length=30))

    class Meta:
        verbose_name = _("allergy")
        verbose_name_plural = _("allergies")

    def __str__(self):
        return "%s: %s" % (self.allergen, self.reaction)

    def as_dict(self):
        return {
            "allergen": self.allergen,
            "reaction": self.reaction,
        }
