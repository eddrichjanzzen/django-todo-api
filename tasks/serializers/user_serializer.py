from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import AuthenticationFailed
from datetime import timedelta


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'email', 'display_name', 'avatar', 'created_date', 'updated_date']

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['display_name']

class UserUploadAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['avatar']


class UserSignUpSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'display_name','tokens', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            display_name=validated_data['display_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    
    def get_tokens(self, obj):
        return obj.tokens()
    

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    display_name = serializers.CharField(read_only=True)
    tokens = serializers.DictField(read_only=True)
    created_date = serializers.DateTimeField(read_only=True)
    updated_date = serializers.DateTimeField(read_only=True)

    class Meta: 
        model = User
        fields = ['id', 'email', 'display_name', 'tokens', 'password', 'created_date', 'updated_date']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(email=email, password=password)
        
        if not user: 
            raise AuthenticationFailed('Invalid credentials, please try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled, please contact admin')


        return {
            'id': user.id,
            'email': user.email,
            'display_name': user.display_name,
            'created_date': user.created_date,
            'updated_date': user.updated_date,
            'tokens': user.tokens(),
        }