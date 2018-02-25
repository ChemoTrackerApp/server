# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from watson import search as watson

class PatienteducationConfig(AppConfig):
    name = 'patienteducation'

    def ready(self):
    	post_model = self.get_model("Post")
    	watson.register(post_model, fields=("title", "content"), store=("url",))
