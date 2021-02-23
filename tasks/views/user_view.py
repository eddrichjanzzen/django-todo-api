from django.contrib.auth.models import User
from rest_framework import generics, permissions
from tasks.serializers import user_serializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializer.UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = user_serializer.UserSerializer
