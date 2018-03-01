from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from symptomtracker.models import Symptom, SymptomGrade, PatientSymptomGrade
from symptomtracker.serializers import PatientSymptomGradeSerializer
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
    # patient_id = request.body.get('patient')
    # symptom_id = request.body.get('symptom')
    # symptom_grade_id = request.body.get('symptom_grade')

    # if symptom_id is None or patient_id is None or symptom_grade_id is None:
    #     errors = ''
    #     if symptom_id is None:
    #         errors+= 'symptom_id\n'
    #     if patient_id is None:
    #         errors+= 'patient_id\n'
    #     if symptom_grade_id is None:
    #         errors+= 'symptom_grade_id\n'
    #     return HttpResponseBadRequest('Missing URL Parameters\n' + errors)

    # created = PatientSymptomGrade.create(patient_id, symptom_id, symptom_grade_id)

    # if (created is None):
    #     return HttpResponseBadRequest('Unable to create symptom')
    # else:
    #     return HttpResponse(json.dumps({"symptom": created}), status=201, content_type='application/json')


    # symptom = Symptom.objects.get(id=symptom_id)
    # patient = Patient.objects.get(id=patient_id)
    data = JSONParser().parse(request)
    serializer = PatientSymptomGradeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)