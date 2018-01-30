from rest_framework import serializers
from symptomtracker.models import PatientSymptomGrade

class PatientSymptomGradeSerializer (serializers.ModelSerializer):
	class Meta:
		model = PatientSymptomGrade
		fields = ('id', 'patient', 'symptom', 'symptom_grade', 'recorded_at')