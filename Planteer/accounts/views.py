from django.shortcuts import render ,redirect
from django.http import HttpRequest

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.


def sign_in(request : HttpRequest):

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"]
        )

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "/"))

        else:
            messages.error(request, "Invalid username or password.", "alert-danger")

    return render(request, "accounts/signin.html")

    
    


def sign_up(request : HttpRequest):
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(
                username=request.POST["username"],
                password=request.POST["password"],
                email=request.POST["email"],
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"]
            )
            new_user.save()
            messages.success(request, "Registered Successfully", "alert-success")
            return redirect("accounts:sign_in")

        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong, try again.", "alert-danger")

    return render(request, "accounts/signup.html", {})


def log_out(request : HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully", "alert-warning")

    return redirect(request.GET.get("next", "/"))
