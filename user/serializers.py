import re
import uuid
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from rest_framework.serializers import ModelSerializer, ValidationError

from user.models import User


class UserCreateSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'email', 'password']

  def validate_username(self, value):
    if not re.search(r'^.{4,150}$', value):
      raise ValidationError('username must between 4 and 150 characters long')
    return value

  def validate_password(self, value):
    if not re.search(r'^.{8,}$', value):
      raise ValidationError('password must have at least 8 characters')  
    if not re.search(r'^(?=.*[a-z])((?=.*[A-Z])|(?=.*\d)|(?=.*[@$!%*#?&_+-]))[A-Za-z\d@$!%*#?&_+-]{8,}$', value):
      raise ValidationError('password must contain 2 of the following: lower letter, upper letter, number, special character in @$!%*#?&_+-')
    return value

  def validate_email(self, value):
    validate_email(value=value)
    return value

  def create(self, validated_data):
    return User.objects.create(
      id=uuid.uuid4(),
      username=validated_data.get('username'),
      email=validated_data.get('email'),
      password=make_password(validated_data.get('password'), 'pbkdf2_sha256')
    ) 


class LoginUserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['username', 'password']


class BasicUserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['username']
  