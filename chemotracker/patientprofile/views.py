from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseForbidden
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from patientprofile.models import PatientProfile
import json

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

    response = [ obj.as_dict() for obj in profile ]

    return HttpResponse(json.dumps({"profile": response}), content_type='application/json')

def update_profile(request):
    user = request.user
    if user is None or not user.is_authenticated:
        return HttpResponseForbidden("Missing or invalid Authorization token")

    print(request.POST)
    request_body = request.body
    print (request_body)
    
    # Parse the json
    body = json.loads(request_body)
    print (body)


@require_http_methods(["GET"])
def users(request):
    query = request.GET.get('query')
    
    if query is None:
        users = PatientProfile.objects.all()[:10]
    else:
        users = PatientProfile.objects.filter(Q(user__first_name__icontains=query) | Q(user__last_name__icontains=query) | Q(user__email__icontains=query))

    response = [ obj.as_dict() for obj in users ]

    return HttpResponse(json.dumps({"users": response}), content_type='application/json')