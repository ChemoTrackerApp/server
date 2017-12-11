# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import PatientUser

class PatientUserView(viewsets.ModelViewSet):
    model = PatientUser
 
    def get_permissions(self):
        # allow non-authenticated user to create via POST
        return (AllowAny() if self.request.method == 'POST'

    @api_view(["POST"])
    def login(request):
        serializer = PatientUserLoginSerializer()  
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


    @api_view(["POST"])
    def register_patient (request):
        username = request.data.get("username")
        password = request.data.get("password") # https://docs.djangoproject.com/en/dev/topics/auth/passwords/
        first_name = request.data.get("firstName")
        last_name = request.data.get("lastName")
        email = request.data.get("email")
        is_staff = False
        is_active = True
        is_superuser = False

        if not username or not password or not first_name or not last_name or not email:
            return Response({"error": "Error Registering User"}, status=HTTP_400_BAD_REQUEST)

        return Response()