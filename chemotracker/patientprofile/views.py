from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from patientprofile.models import PatientProfile, Allergy
import json
import time
import datetime

@require_http_methods(["GET", "POST"])
@csrf_exempt
def profile(request):
    if request.method == 'GET':
        return get_profile(request)
    elif request.method == 'POST':
        return update_profile(request)

def get_profile(request):
    if request.user is None or not request.user.is_authenticated:
        return HttpResponseForbidden("Missing or invalid Authorization token")

    print (request.user.id)
    profile = PatientProfile.objects.filter(user_id=request.user.id)

    return HttpResponse(json.dumps(profile[0].as_dict()), content_type='application/json')

def update_profile(request):
    user = request.user
    if user is None or not user.is_authenticated:
        return HttpResponseForbidden("Missing or invalid Authorization token")

    
    request_body = request.body
    
    # Parse the json
    body = json.loads(request_body)

    email = body.get('emailAddress')
    first_name = body.get('firstName')
    last_name = body.get('lastName')
    image = body.get('image')
    medical_conditions = body.get('medicalConditions')
    medication_list = body.get('medicationList')
    allergy = body.get('allergy')
    cancer_diagnosis = body.get('cancerDiagnosis')
    gender = body.get('gender')
    date_of_birth = datetime.datetime.strptime(body.get('dateOfBirth'), '%Y-%m-%d').date() 
    phone_number = body.get('phoneNumber')
    chemotherapy = body.get('chemotherapy')
    try:
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.patientprofile.image = image
        user.patientprofile.medical_conditions = medical_conditions
        user.patientprofile.medication_list = medication_list
        user.patientprofile.cancer_diagnosis = cancer_diagnosis
        user.patientprofile.gender = gender
        user.patientprofile.date_of_birth = date_of_birth
        user.patientprofile.phone_number = phone_number

        # Delete existing allergies
        Allergy.objects.filter(patient_id=user.patientprofile).delete()

        for a in allergy:
            temp = Allergy()
            temp.patient = user.patientprofile
            temp.allergen = a.get('allergen')
            temp.reaction = a.get('reaction')
            temp.save()

        user.patientprofile.chemotherapy = chemotherapy
        user.save()
        user.patientprofile.save()
    except Exception:
        return HttpResponseBadRequest("Invalid data.")
    
    return HttpResponse(json.dumps(user.patientprofile.as_dict()), content_type='application/json')    



@require_http_methods(["GET"])
def users(request):
    query = request.GET.get('query')
    
    if query is None:
        users = PatientProfile.objects.all()[:10]
    else:
        users = PatientProfile.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__email__icontains=query))

    response = [ obj.as_dict() for obj in users ]

    return HttpResponse(json.dumps({"users": response}), content_type='application/json')