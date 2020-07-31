from rest_framework.authtoken.models import Token
from rest_framework import serializers, viewsets
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)

class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'phone', 'address', 'is_active', 'is_superuser', 'auth_token')
        read_only_fields = ('id', 'is_active', 'is_superuser')
    
    def get_auth_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

class EmptySerializer(serializers.Serializer):
    pass

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name')

    def validate_email(self, value):
        user = User.objects.filter(email=value)
        if user:
            raise serializers.ValidationError("Email is already taken")
        return BaseUserManager.normalize_email(value)

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError('Current password does not match')
        return value
    
    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    """
    A user serializer for get profile of user
    """

    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'picture_url','address')
        read_only_fields = ('email', )

