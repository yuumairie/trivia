from rest_framework import serializers
from .models import Haiku, Profile, Comment, Good
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ('id', 'email', 'password', 'username')
    extra_kwargs = {
        'password': {'write_only': True, 'required': True},
        'email': {'write_only': True},
    }

  def create(self, validated_data):
    user = get_user_model().objects.create_user(**validated_data)
    return user


class ProfileSerializer(serializers.ModelSerializer):
  created_on = serializers.DateTimeField(
      format='%Y-%m-%d %H:%M', read_only=True)

  class Meta:
    model = Profile
    fields = ('id', 'nickName', 'userProfile', 'created_on', 'img')
    extra_kwargs = {'userProfile': {'read_only': True}}


class GoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = Good
    fields = (
        'id',
        'user',
        'haiku',
    )


class HaikuWriteSerializer(serializers.ModelSerializer):
  class Meta:
    model = Haiku
    fields = (
        'id',
        'userPost',
        'content',
        'created_at',
        'good',
    )
    extra_kwargs = {'userPost': {'read_only': True}}


class HaikuReadSerializer(serializers.ModelSerializer):
  userPost = UserSerializer(read_only=True)
  good = UserSerializer(many=True)
  created_at = serializers.DateTimeField(format='%Y/%m/%d')

  class Meta:
    model = Haiku
    fields = (
        'id',
        'userPost',
        'content',
        'created_at',
        'good',
    )
    extra_kwargs = {'userPost': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ('id', 'text', 'userComment', 'post')
    extra_kwargs = {'userComment': {'read_only': True}}
