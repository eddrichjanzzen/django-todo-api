from tasks.models import Task
from rest_framework import generics, permissions
from tasks.serializers import task_serializer

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = task_serializer.TaskSerializer
    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = task_serializer.TaskSerializer
    permission_classes = []