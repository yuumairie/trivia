from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


def upload_avatar_path(instance, filename):
  ext = filename.split('.')[-1]
  return f'avatars/{instance.userProfile.id}{instance.nickName}.{ext}'


def upload_post_path(instance, filename):
  ext = filename.split('.')[-1]
  return f'posts/{instance.userPost.id}{instance.content}.{ext}'


class UserManager(BaseUserManager):
  def create_user(self, email, password, username='', **extra_fields):

    if not email:
      raise ValueError('email is must')

    user = self.model(
        email=self.normalize_email(email), username=username, **extra_fields
    )
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self, email, password, username='', **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    return self.create_user(email, password, username, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(max_length=50, unique=True)
  username = models.CharField(max_length=20, blank=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'

  def __str__(self):
    return self.email


class Profile(models.Model):
  nickName = models.CharField(max_length=20)
  userProfile = models.OneToOneField(
      settings.AUTH_USER_MODEL, related_name='userProfile', on_delete=models.CASCADE
  )
  created_on = models.DateTimeField(auto_now_add=True)
  img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

  def __str__(self):
    return self.nickName


class Haiku(models.Model):
  userPost = models.ForeignKey(
      settings.AUTH_USER_MODEL, related_name='userPost', on_delete=models.CASCADE
  )
  content = models.CharField(max_length=50)
  good = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Good')
  created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
  text = models.CharField(max_length=100)
  userComment = models.ForeignKey(
      settings.AUTH_USER_MODEL, related_name='userComment', on_delete=models.CASCADE
  )
  post = models.ForeignKey(Haiku, on_delete=models.CASCADE)

  def __str__(self):
    return self.text


class Good(models.Model):
  user = models.ForeignKey(
      settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE,
      related_name='user_relationships',
  )
  haiku = models.ForeignKey(
      Haiku, on_delete=models.CASCADE, related_name='haiku_relationships'
  )

  class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'haiku'], name='unique_set')
    ]
