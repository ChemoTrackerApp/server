from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from patientprofile.models import PatientProfile
import json

@require_http_methods(["GET", "POST"])
def profile(request):
    if request.method == 'GET':
        return get_profile(request)
    elif request.method == 'POST':
        return update_profile(request)

def get_profile(request):
    user = request.user
    if user is None or not user.is_authenticated:
        return HttpResponseForbidden("Missing or invalid Authorization token")

    return HttpResponse(json.dumps(user.patientprofile.as_dict()), content_type='application/json')

def update_profile(request):
    user_id = request.GET.get('id')
    if user_id is None:
        return HttpResponseBadRequest('Need to specify user_id as URL Parameter')

    user = PatientProfile.objects.get(user=user_id)

    request_body = request.body
    
    # Parse the json
    body = json.loads(request_body)

    first_name = body['firstName']
    last_name = body['lastName']

@require_http_methods(["GET"])
def users(request):
    query = request.GET.get('query')
    
    if query is None:
        users = PatientProfile.objects.all()[:10]
    else:
        users = PatientProfile.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__email__icontains=query))

    response = [ obj.as_dict() for obj in users ]

    return HttpResponse(json.dumps({"users": response}), content_type='application/json')