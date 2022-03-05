import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  id = models.UUIDField(primary_key=True, editable=False)
  email = models.EmailField(unique=True, null=True)
  is_active = models.BooleanField(default=False)


class ShortToken(models.Model):
  id = models.CharField(max_length=10, primary_key=True)
  created_time = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
      return self.id