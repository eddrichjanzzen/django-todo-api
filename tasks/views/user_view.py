from django.contrib.auth.models import User
from rest_framework import generics, permissions, status, views
from tasks.serializers import user_serializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from cloudinary import CloudinaryResource
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

class UserMeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = user_serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def update(self, request, *args, **kwargs):
        
        instance = self.get_object()
        serializer = user_serializer.UserUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)        

        user_data = self.get_serializer(instance)

        response = {
            'success': True,
            'data': user_data.data
        }

        return Response(response, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()

        if instance:
            cloudinary.uploader.destroy(instance.cloudinary_public_id(), invalidate=True)
            self.perform_destroy(instance)        
        
        response = {
            'success': True
        }

        return Response(response, status=status.HTTP_204_NO_CONTENT)

class UserUploadDeleteAvatar(generics.GenericAPIView):
    model = User
    serializer_class = user_serializer.UserUploadAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]

    parser_classes = [
        MultiPartParser,
        JSONParser
    ]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj

    def post(self, request):

        file = request.data.get('avatar', None)
        success = False
        upload_data = {}

        try:
            upload_data = cloudinary.uploader.upload(
                    file, 
                    folder='todo_avatars/'
                )

            # update the user avatar url
            instance = self.get_object()
            serializer = self.get_serializer(instance, data={
                'avatar': upload_data['url']
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            success = True

        except Exception as e:
            response = {
                'success': success,
                'error': 'A problem occured when uploading file: {}'.format(e)
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': success,
            'data': {
                'name': upload_data['public_id'],
                'url': upload_data['url']
            }
        }

        return Response(response, status=status.HTTP_200_OK)

    def delete(self, request):
        success = False
        try:

            instance = self.get_object()
            cloudinary.uploader.destroy(instance.cloudinary_public_id(), invalidate=True)

            serializer = self.get_serializer(instance, data={
                'avatar': ''
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            success = True

        except Exception as e:
            response = {
                'success': success,
                'error': 'A problem occured while deleting file: {}'.format(e)
            }

            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        response = {
            'success': success
        }

        return Response(response, status=status.HTTP_200_OK)
