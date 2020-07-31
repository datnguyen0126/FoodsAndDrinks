from django.contrib.auth import authenticate, get_user_model, logout
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from rest_framework import viewsets, status, generics, permissions, views
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from . import serializers
from .service import user_service

from django.http import JsonResponse
from requests.exceptions import HTTPError


User = get_user_model()

class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_classes = {
        'login': serializers.UserLoginSerializer,
        'register': serializers.UserRegisterSerializer,
        'admin_register': serializers.UserRegisterSerializer,
        'logout': serializers.EmptySerializer,
        'password_change': serializers.PasswordChangeSerializer,
        'profile': serializers.UserProfileSerializer,
        'profile_picture': serializers.UserProfileSerializer,
    }

    @action(methods=['POST'], detail=False, url_path='auth/login')
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = user_service.get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='user/register')
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
        
    @action(methods=['POST'], detail=False, url_path='admin/register')
    def admin_register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_superuser(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=False, url_path='auth/logout')
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        data = {'message': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, url_path='user/changepassword', permission_classes=[IsAuthenticated])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'PUT'], detail=False, url_path='user/profile', permission_classes=[IsAuthenticated])
    def profile(self, request):
        if request.method == 'GET':
            user = User.objects.get(pk=request.user.id)
            user_serializer = serializers.UserProfileSerializer(user).data
            return Response(data=user_serializer, status=status.HTTP_200_OK)
        elif request.method == 'PUT':
            profile_serializer = self.get_serializer(data=request.data)
            profile_serializer.is_valid(raise_exception=True)
            try:
                user = User.objects.filter(pk=request.user.id).update(**profile_serializer.validated_data)
            except ObjectDoesNotExist:
                data = {'message': 'User not found'}
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            data = {'message': 'Update profile successfully'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False, url_path='user/profile/picture', permission_classes=[IsAuthenticated])
    def profile_picture(self, request):
        try:
            file = request.data['file']
            user = User.objects.get_user(request.user.id)
            if user:
                user.picture_url = file
                user.save()
                picture_serializer = serializers.UserProfileSerializer(user).data
                return Response(data=picture_serializer, status=status.HTTP_204_NO_CONTENT)
            data = {'message': 'User not found'}
            return Response(data, status=status.HTTP_404_NOT_FOUND)                    
        except KeyError:
            data = {'message': 'Request has no resource file attached'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


            
