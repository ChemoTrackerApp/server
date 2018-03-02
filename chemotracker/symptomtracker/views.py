from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from symptomtracker.models import Symptom, SymptomGrade, PatientSymptomGrade
from symptomtracker.serializers import PatientSymptomGradeSerializer
import time
import datetime
import json

@require_http_methods(["GET", "POST"])
@csrf_exempt
def symptoms(request):
    if request.method == 'GET':
        symptoms = Symptom.objects.all()
        response = [ obj.as_dict() for obj in symptoms ]
        return HttpResponse(json.dumps({"symptom": response}), content_type='application/json')
    elif request.method == 'POST':
        return add_symptom(request)

@require_http_methods(["GET"])
def grades(request):
    print (request)
    print(request.user)
    symptom_id = request.GET.get('symptom')
    if symptom_id is None:
        return HttpResponseBadRequest('Need to specify symptom id as URL Parameter')

    symptom = Symptom.objects.get(id=symptom_id)

    if symptom is None:
        return HttpResponseNotFound('Symptom not found!')

    grades = SymptomGrade.objects.filter(symptom=symptom)

    response = [ obj.as_dict() for obj in grades ]

    return HttpResponse(json.dumps({symptom.name: response}), content_type='application/json')

def add_symptom(request):
    data = JSONParser().parse(request)
    serializer = PatientSymptomGradeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@require_http_methods(["GET"])
def get_patient_symptoms(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')
