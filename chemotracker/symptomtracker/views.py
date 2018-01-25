from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from symptomtracker.models import Symptom, SymptomGrade
import json

@require_http_methods(["GET"])
def symptoms(request):
    symptoms = Symptom.objects.all()
    response = [ obj.as_dict() for obj in symptoms ]
    return HttpResponse(json.dumps({"data": response}), content_type='application/json')

@require_http_methods(["GET"])
def grades(request):
    symptom_name = request.GET.get('symptom')
    if symptom_name is None:
        return HttpResponseBadRequest('Need to specify symptom as URL Parameter')

    symptom = Symptom.objects.get(name=symptom_name)

    if symptom is None:
        return HttpResponseBadRequest('Symptom not found!')

    grades = SymptomGrade.objects.filter(symptom=symptom)

    response = [ obj.as_dict() for obj in grades ]

    return HttpResponse(json.dumps({symptom.name: response}), content_type='application/json')

