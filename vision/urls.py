from django.urls import path

from vision.views import VisionCrudView
urlpatterns = [
    path('', VisionCrudView.as_view()),
]