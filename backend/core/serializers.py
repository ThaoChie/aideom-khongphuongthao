from rest_framework import serializers
from .models import LessonRun
class LessonRunSerializer(serializers.ModelSerializer):
    class Meta:
        model=LessonRun
        fields='__all__'
