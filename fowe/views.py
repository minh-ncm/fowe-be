from django.shortcuts import render
from django.views.decorators.cache import never_cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


def index(request):
  return render(request, 'index.html')

class DisabledView(GenericAPIView):
  def post(self, request, format=None):
    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

  def get(self, request, format=None):
    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

  def put(self, request, format=None):
    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

  def patch(self, request, format=None):
    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

  def delete(self, request, format=None):
    return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)