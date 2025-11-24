from django.urls import path

from .models import CustomUser
from .views import UserLoginView, UserRegisterView, user_logout

app_name = "account"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", user_logout, name="logout"),
]