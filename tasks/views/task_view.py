from tasks.models import Task
from rest_framework import generics, permissions, status
from tasks.serializers import task_serializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class TaskList(generics.ListCreateAPIView):

    serializer_class = task_serializer.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        
        title = self.request.query_params.get('title', None)
        completed = self.request.query_params.get('completed', None)

        tasks = Task.objects.filter(owner=self.request.user).order_by('-created_date')

        # filter by title
        if title is not None: 
            tasks = tasks.filter(title__icontains=title)
        
        if completed is not None:
            tasks = tasks.filter(completed=completed)

        return tasks


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response = {
            'success' : True,
            'data': serializer.data
        }

        return Response(response, status=status.HTTP_201_CREATED)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = task_serializer.TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = task_serializer.TaskDetailSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        response = {
            'success': True,
            'data': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):

        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response = {
            'success': True,
            'data': serializer.data 
        }

        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        self.perform_destroy(instance)        

        response = {
            'success': True
        }

        return Response(response, status=status.HTTP_204_NO_CONTENT)
