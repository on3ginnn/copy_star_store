from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .forms import UserRegisterForm
from .models import CustomUser


class UserRegisterView(CreateView):
    template_name = "registration/register.html"
    form_class = UserRegisterForm
    model = CustomUser
    success_url = reverse_lazy("store:homepage")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)
    

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "registration/login.html"
    success_url = reverse_lazy("store:homepage")
    
    def get_success_url(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return reverse_lazy('store:admin-dashboard')
        return self.success_url
    

def user_logout(request):
    logout(request)
    return redirect('store:homepage')