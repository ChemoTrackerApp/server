# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.views.decorators.http import require_http_methods
from patienteducation.models import Post
from watson import search as watson
import json

@require_http_methods(["GET"])
def posts(request):
    query_text = request.GET.get('query')
    if query_text is None:
        return HttpResponseBadRequest('Need to specify query as URL Parameter')

    posts = watson.search(query_text, models=(Post,))

    # if posts is None:
    #     return HttpResponseNotFound('No match found!')

    response = []
    for post in posts:
    	response.append({
    		"title": post.title,
    		"url": post.object.url,
    		"content": post.content[:100]
    	})

    return HttpResponse(json.dumps({"posts": response}), content_type='application/json')