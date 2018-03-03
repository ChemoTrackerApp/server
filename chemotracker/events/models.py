from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Event(models.Model):
	creator = models.ForeignKey(User, on_delete=models.CASCADE)
	start = models.DateTimeField()
	end = models.DateTimeField()
	creation_date = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=256)
	notes = models.TextField()

	class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    def __str__(self):
        return "%s" % (self.title)

	def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start.strftime('%Y-%m-%d %H:%M:%S'),
            "end": self.end.strftime('%Y-%m-%d %H:%M:%S'),
            "notes": self.notes,
            "creation_date": self.creation_date.strftime('%Y-%m-%d %H:%M:%S')
        }
