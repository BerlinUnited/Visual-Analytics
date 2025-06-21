from django.urls import path
from .views import LoginView, LogoutView, SignupView

urlpatterns = [
    path("login", LoginView, name="mylogin"),
    path("logout", LogoutView, name="mylogout"),
    path("signup", SignupView, name="signup"),
]
