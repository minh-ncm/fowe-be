import random
from django.contrib.auth import authenticate
from django.core.mail import EmailMessage
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from fowe import settings
from user.models import ShortToken, User
from user.serializers import UserCreateSerializer


def generate_short_token(length=10, seed=None):
  """
  Generate short random token.
  Current random character include number, upper and lower letter
  Args:
    length: token's length
    seed: random seeds
  Return:
    token: a string of randomly generated token
  """
  anscii = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))
  random.seed(seed)
  while True:
    try:
      generated_token = ''.join([chr(random.choice(anscii)) for _ in range(length)])
      ShortToken.objects.get(id=generated_token)
    except ShortToken.DoesNotExist as e:
      return generated_token


def send_activate_email(user):
  """
  Send an email include a token to activate user's account
  Args: 
    user: instance of django model
  Returns:
    None
  """
  token = generate_short_token()
  ShortToken.objects.create(id=token, user=user).save()
  msg = EmailMessage(
    subject='Verify email',
    body=f'Token: {token}',
    from_email=settings.EMAIL_HOST_USER,
    to=[user.email]
  )
  msg.send()


class UserLoginView(GenericAPIView):
  def post(self, request, *args, **kwargs):
    username = request.data.get('username')
    password = request.data.get('password')
    authenticate(username=username, password=password)
    return Response("ok", status=status.HTTP_200_OK)


class UserLogoutView(GenericAPIView):
  def post(self, request, *args, **kwargs):
    try:
      token = RefreshToken(request.data.get('refresh_token'))
      token.blacklist()
    except Exception:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
      return Response(status=status.HTTP_200_OK)


class UserActivateView(APIView):
  def get(self, request, *args, **kwargs):
    params = request.query_params
    token = params.get('token')
    username = params.get('username')
    if username: 
      try:
        user = User.objects.get(username=username)
      except User.DoesNotExist:
        return Response(data='Username not found. Please check again', status=status.HTTP_400_BAD_REQUEST)
      else:
        send_activate_email(user)
        return Response(status=status.HTTP_202_ACCEPTED)
      
    if token:
      try:        
        short_token = ShortToken.objects.get(id=token)        
      except ShortToken.DoesNotExist:
        return Response(data='Token not found. Please check your token again', status=status.HTTP_400_BAD_REQUEST)
      else:
        user = short_token.user
        user.is_active = True
        short_token.delete()
        user.save()
        short_token.save()
        return Response(status=status.HTTP_200_OK)
    else:
      return Response(data='Token not found', status=status.HTTP_400_BAD_REQUEST)

  
class UserCrudView(GenericAPIView):
  def post(self, request, format=None):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      send_activate_email(user)
      return Response(serializer.data, status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def get(self, request, format=None):
    return Response(status=status.HTTP_200_OK)