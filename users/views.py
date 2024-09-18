from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from users.forms import UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(View):
    def get(self, request):
        create_form = UserCreateForm()
        context = {
            "form": create_form
        }
        return render(request, 'users/Register.html', context)

    def post(self, request):

        create_form = UserCreateForm(data=request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('users:login')
        else:
            context = {
                "form": create_form
            }
            return render(request, 'users/Register.html', context)

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()

        return render(request, 'users/Login.html', {"login_form": login_form})

    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect("books:list")

        else:
            return render(request, 'users/Login.html', {"login_form": login_form})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'users/profile.html', {'user': request.user})



class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('landing_page')


