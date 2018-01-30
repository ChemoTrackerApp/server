from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from symptomtracker.models import Symptom, SymptomGrade, PatientSymptomGrade
from symptomtracker.serializers import PatientSymptomGradeSerializer
import json

@require_http_methods(["GET", "POST"])
def symptoms(request):
    if request.method == 'GET':
        symptoms = Symptom.objects.all()
        response = [ obj.as_dict() for obj in symptoms ]
        return HttpResponse(json.dumps({"symptom": response}), content_type='application/json')
    elif request.method == 'POST':
        return add_symptom(request)

@require_http_methods(["GET"])
def grades(request):
    symptom_name = request.GET.get('symptom')
    if symptom_name is None:
        return HttpResponseBadRequest('Need to specify symptom as URL Parameter')

    symptom = Symptom.objects.get(name=symptom_name)

    if symptom is None:
        return HttpResponseNotFound('Symptom not found!')

    grades = SymptomGrade.objects.filter(symptom=symptom)

    response = [ obj.as_dict() for obj in grades ]

    return HttpResponse(json.dumps({symptom.name: response}), content_type='application/json')

def add_symptom(request):
    serializer = PatientSymptomGradeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)