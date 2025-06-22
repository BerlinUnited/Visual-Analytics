from django.urls import path
from .views import LoginView, LogoutView, SignupView,verify_email

urlpatterns = [
    path("login", LoginView, name="mylogin"),
    path("logout", LogoutView, name="mylogout"),
    path("signup", SignupView, name="signup"),
    path('verify-email/<uuid:token>/', verify_email, name='verify_email'),
]
