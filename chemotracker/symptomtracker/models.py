from django.db import models
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
