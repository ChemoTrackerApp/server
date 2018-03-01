# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Post(models.Model):
    title = models.TextField()
    url = models.URLField()
    content = models.TextField()

    class Meta:
        verbose_name = _("patient education post")
        verbose_name_plural = _("patient education posts")

    def __str__(self):
        return "%s" % (self.title)

    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
        }