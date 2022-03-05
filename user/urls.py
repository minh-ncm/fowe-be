from django.urls import path

from user.views import UserLoginView, UserLogoutView, UserActivateView, UserCrudView


urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('logout/', UserLogoutView.as_view()),
    path('activate/', UserActivateView.as_view(), name='user_activate'),
    path('crud/', UserCrudView.as_view()),
]
