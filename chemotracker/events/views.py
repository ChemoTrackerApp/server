from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from events.models import Event
import time
import datetime
import json


@require_http_methods(["GET", "POST"])
def event(request):
	if request.method == 'GET':
        return get_event(request)
    elif request.method == 'POST':
        return create_event(request)

def get_event(request):
	if request.user is None or not request.user.is_authenticated:
		return HttpResponseForbidden("Missing or invalid Authorization token")

	year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    if year is None or month is None or day is None:
        return HttpResponseBadRequest("Missing year or month or day field")

    try:
        query_date = datetime.date(int(year), int(month), int(day))
    except ValueError:
        return HttpResponseBadRequest("Invalid date")
    except Exception:
        return HttpResponseBadRequest("Invalid date. Parameters must be invalid.")


	events = Event.objects.filter(Q(start__date=query_date) | Q(end__date=query_date) )

	response = [ obj.as_dict() for obj in events ]

	HttpResponse(json.dumps({"events": response}), content_type='application/json')

def create_event(request):
	if request.user is None or not request.user.is_authenticated:
		return HttpResponseForbidden("Missing or invalid Authorization token")

	data = JSONParser().parse(request)

	start_year = data['startYear']
	start_month = data['startMonth']
	start_day = data['startDay']
	# Need start time
	end_year = data['endYear']
	end_month = data['endMonth']
	end_day = data['endDay']
	# Need end time

	try:
        start_date = datetime.date(int(start_year), int(start_month), int(start_day))
    except ValueError:
        return HttpResponseBadRequest("Invalid date")
    except Exception:
        return HttpResponseBadRequest("Invalid date. Parameters must be invalid.")


	title = data['title']

