from django.contrib.auth.models import User
from rest_framework import generics, permissions
from tasks.serializers import user_serializer
from django.contrib.auth import get_user_model

User = get_user_model()

class UserList(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = user_serializer.UserSerializer


class UserSignUp(generics.CreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = user_serializer.UserSignUpSerializer
    permission_classes = [permissions.AllowAny]

class UserLogin(generics.CreateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = user_serializer.UserLoginSerializer
    permission_classes = [permissions.AllowAny]

class UserGetDetails(generics.RetrieveAPIView):
    serializer_class = user_serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user)
