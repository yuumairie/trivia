from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.conf import settings

def upload_avatar_path(instance,filename):
  ext = filename.split('.')[-1]
  return '/'.join(['avatars',str(instance.userProfile.id)+str(instance.nickName)+str(".")+str(ext)])

def upload_post_path(instance,filename):
  ext = filename.split('.')[-1]
  return '/'.join(['posts',str(instance.userPost.id)+str(instance.content)+str(".")+str(ext)])

class UserManager(BaseUserManager):
  def create_user(self,email,password,username):

    if not email:
      raise ValueError('email is must')

    user = self.model(email=self.normalize_email(email),username=username)
    user.set_password(password)
    user.save(using=self._db)

    return user

  def create_superuser(self,email,password):
    user = self.create_user(email,password)
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)

    return user

class User(AbstractBaseUser,PermissionsMixin):
  email = models.EmailField(max_length=50,unique=True)
  username = models.CharField(max_length=20,blank=True)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)

  objects = UserManager()

  USERNAME_FIELD = 'email'

  def __str__(self):
    return self.email

class Profile(models.Model):
  nickName = models.CharField(max_length=20)
  userProfile = models.OneToOneField(
    settings.AUTH_USER_MODEL,related_name='userProfile',
    on_delete=models.CASCADE
  )
  created_on = models.DateTimeField(auto_now_add=True)
  img = models.ImageField(blank=True,null=True,upload_to=upload_avatar_path)

  def __str__(self):
    return self.nickName

class Genre(models.Model):
  name = models.CharField(max_length=25)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

class Trivia(models.Model):
  userPost = models.ForeignKey(
    settings.AUTH_USER_MODEL, related_name='userPost'
    ,on_delete=models.CASCADE)
  genre = models.ForeignKey(Genre,on_delete=models.CASCADE)
  content = models.TextField(max_length=50)
  explanation = models.CharField(max_length=255,blank=True)
  good = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Good')
  created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
  text = models.CharField(max_length=100)
  userCommnet = models.ForeignKey(
    settings.AUTH_USER_MODEL,related_name='userComment',
    on_delete=models.CASCADE
  )
  post = models.ForeignKey(Trivia,on_delete=models.CASCADE)

  def __str__(self):
    return self.text
  
class Good(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,on_delete=models.CASCADE
    ,related_name='user_relationships'
  )
  trivia = models.ForeignKey(Trivia,on_delete=models.CASCADE
  ,related_name='trivia_relationships'
  )

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['user','trivia'],name='unique_set')
    ]
