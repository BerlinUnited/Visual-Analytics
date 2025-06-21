from user.forms import SignupForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def LoginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next", "events")
            return redirect(next_url)
        else:
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, "frontend/login.html", context)


def SignupView(request):
    form = SignupForm()
    context = {"form": form}

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("mylogin")

    context = {"form": form}
    return render(request, "frontend/signup.html", context)

def LogoutView(request):
    logout(request)
    return redirect("mylogin")
