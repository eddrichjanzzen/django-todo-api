from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from tasks.serializers import user_serializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

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

class UserLogin(generics.GenericAPIView):
    model = User
    serializer_class = user_serializer.UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetProfileDetails(generics.RetrieveAPIView):
    serializer_class = user_serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

class UserUpdateProfileDetails(generics.UpdateAPIView):
    serializer_class = user_serializer.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def update(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        super(UserUpdateProfileDetails, self).update(request, * args, **kwargs)

        response = {
            'success': True 
        }

        return Response(response, status=status.HTTP_200_OK)