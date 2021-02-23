from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        owner = serializers.ReadOnlyField(source='owner.email')
        fields = ['id', 'title', 'description', 'owner', 'deadline', 'created_date', 'updated_date', 'completed']
        