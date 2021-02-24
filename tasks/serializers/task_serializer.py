from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 
            'title', 
            'description', 
            'deadline', 
            'created_date', 
            'updated_date', 
            'completed'
        ]

