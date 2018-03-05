from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _

class Symptom(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("symptom")
        verbose_name_plural = _("symptoms")

    def __str__(self):
        return "%s" % (self.name)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Grade(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("grade")
        verbose_name_plural = _("grades")

    def __str__(self):
        return "%s: %s" % (self.symptom.name, self.name)


class SymptomGrade(models.Model):
    symptom = models.ForeignKey('Symptom', on_delete=models.CASCADE)
    description = models.TextField()
    # grading_patient_friendly = models.TextField()
    # intervention_patient_friendly = models.TextField()
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("symptom grade description")
        verbose_name_plural = _("symptom grade descriptions")

    def __str__(self):
        return "%s: %s" % (self.symptom.name, self.name)

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.grade.name,
            "description": self.description
        }

class PatientSymptomGrade(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    symptom = models.ForeignKey('Symptom', on_delete=models.CASCADE)
    symptom_grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("patient symptom grade")
        verbose_name_plural = _("patient symptom grades")
        ordering = ('recorded_at',)

    def __str__(self):
        return "%s: %s" % (self.symptom.name, self.name)

    def as_dict(self):
        return {
            "patient": self.patient.id,
            "symptom": self.symptom.id,
            "grade": self.symptom_grade.id,
            "recorded_at": self.recorded_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Intervention (models.Model):
    symptom = models.ForeignKey('Symptom', on_delete=models.CASCADE)
    grade = models.ForeignKey('Grade', on_delete=models.CASCADE)
    description = ArrayField(models.TextField(), null=True)

    class Meta:
        verbose_name = _("intervention")
        verbose_name_plural = _("interventions")

    def __str__(self):
        return "Symptom %s and Grade %s: %s" % (self.symptom.name, self.grade.name, self.description)

    def as_dict(self):
        return {
            "symptom": self.symptom.id,
            "grade": self.grade.id,
            "description": self.description
        }


class Tip (models.Model):
    symptom = models.ForeignKey('Symptom', on_delete=models.CASCADE)
    description = ArrayField(models.TextField(), null=True)
    icon = models.CharField(max_length=30)

    class Meta:
        verbose_name = _("tip")
        verbose_name_plural = _("tips")

    def __str__(self):
        return "Symptom %s Icon %s: %s" % (self.symptom.name, self.icon, self.description)

    def as_dict(self):
        return {
            "symptom": self.symptom.id,
            "description": self.description,
            "icon": self.icon
        }