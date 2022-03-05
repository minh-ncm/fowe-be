from django.urls import path

from blog.views import BlogDetailsView, BlogCrudView


urlpatterns = [
    path('details/', BlogDetailsView.as_view()),
    path('crud/', BlogCrudView.as_view()),
]
