from django.urls import path

from users.views import RegisterView, LoginView


app_name = 'users'
urlpatterns = [
    path("Register", RegisterView.as_view(), name='register'),
    path("Login", LoginView.as_view(), name='login'),
]





