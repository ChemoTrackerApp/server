from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from symptomtracker.models import Symptom
import json

@require_http_methods(["GET"])
def symptoms(request):
    symptoms = Symptom.objects.all()
    response = [ obj.as_dict() for obj in symptoms ]
    return HttpResponse(json.dumps({"data": response}), content_type='application/json')
