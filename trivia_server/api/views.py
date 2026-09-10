from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import generics
from .models import Trivia, Genre, Profile, Comment, User,Good
from rest_framework import viewsets
from . import serializers
from .ownpermissions import ProfilePermission


class CreateUserView(generics.CreateAPIView):
  serializer_class = serializers.UserSerializer
  permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
  permission_classes = (ProfilePermission,)
  queryset = Profile.objects.all()
  serializer_class = serializers.ProfileSerializer

  def perform_create(self, selializer):
    selializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = serializers.UserSerializer

  def get_queryset(self):
    return self.queryset.filter(email=self.request.user)


class GenreViewSet(viewsets.ModelViewSet):
  queryset = Genre.objects.all()
  serializer_class = serializers.GenreSerializer
  permission_classes = (AllowAny,)

class GoodViewSet(viewsets.ModelViewSet):
  queryset = Good.objects.all()
  serializer_class = serializers.GoodSerializer
  permission_classes = (IsAuthenticatedOrReadOnly,)
  # def get_queryset(self):
  #   return self.queryset.filter(user=self.request.user)

class TriviaViewSet(viewsets.ModelViewSet):
  permission_classes = (IsAuthenticatedOrReadOnly,)
  queryset = Trivia.objects.all()

  def get_serializer_class(self):
    if self.request.method == 'GET':
      return serializers.TriviaReadSerializer
    return serializers.TriviaWriteSerializer

  def perform_create(self,serializer):
    serializer.save(userPost=self.request.user)
  
class CommentViewSet(viewsets.ModelViewSet):
  queryset = Comment.objects.all()
  serializer_class = serializers.CommentSerializer

  def perform_create(self,selializer):
    serializer.save(userComment=self.request.user)
