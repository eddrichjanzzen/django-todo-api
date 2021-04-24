from rest_framework import serializers
from tasks.models import Task

class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'created_date', 'updated_date', 'completed']
        read_only_fields = ['id']
        
class TaskDetailSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline', 'created_date', 'updated_date', 'completed']