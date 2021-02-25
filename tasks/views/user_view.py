from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, views
from tasks.serializers import user_serializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
import cloudinary.uploader

User = get_user_model()

class UserList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
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


class UserGetProfileDetail(generics.RetrieveAPIView):
    serializer_class = user_serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

class UserUpdateProfileDetail(generics.UpdateAPIView):
    serializer_class = user_serializer.UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)        

        response = {
            'success': True,
            'data': serializer.data
        }

        return Response(response, status=status.HTTP_200_OK)


class UserUploadAvatar(generics.GenericAPIView):
    model = User
    serializer_class = user_serializer.UserUploadAvatarSerializer
    permission_classes = [permissions.AllowAny]

    parser_classes = (
        MultiPartParser,
        JSONParser
    )

    def post(self, request):
        file = request.data.get('avatar', None)
        success = False
        upload_data = {}

        try:
            upload_data = cloudinary.uploader.upload(file)
            success = True

        except Exception as e:
            print(e)
            success = False
            upload_data = {}

        response = {
            'success': success,
            'data': upload_data
        }

        return Response(response, status=status.HTTP_200_OK)

class UploadView(views.APIView):
    parser_classes = (
        MultiPartParser,
        JSONParser,
    )

    @staticmethod
    def post(request):
        file = request.data.get('avatar')

        upload_data = cloudinary.uploader.upload(file)
        return Response({
            'status': 'success',
            'data': upload_data,
        }, status=201)