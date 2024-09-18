from django.urls import path

from users.views import RegisterView, LoginView, ProfileView

app_name = 'users'
urlpatterns = [
    path("Register/", RegisterView.as_view(), name='register'),
    path("Login/", LoginView.as_view(), name='login'),
    path("Profile/", ProfileView.as_view(), name='profile')
]





