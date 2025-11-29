from django.shortcuts import render ,redirect
from django.http import HttpRequest

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import UserProfile
from django.db import transaction
from plants.models import Review




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

    
    


def sign_up(request: HttpRequest):

    if request.method == "POST":

        try:
            with transaction.atomic():

                new_user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password"],
                    email=request.POST["email"],
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"]
                )
                new_user.save()

                profile = UserProfile(
                    user=new_user,
                    bio=request.POST.get("bio", ""),
                    website=request.POST.get("website", ""),
                    profile_picture=request.FILES.get(
                        "profile_picture",
                        UserProfile.profile_picture.field.get_default()
                    )
                )
                profile.save()

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



def user_profile_view(request:HttpRequest, user_name):

    try:
        profile_user = User.objects.get(username=user_name)

        if not UserProfile.objects.filter(user=profile_user).first():
            new_profile = UserProfile(user=profile_user)
            new_profile.save()
               
               
        user_reviews = Review.objects.filter(user=profile_user).select_related("plant")
        review_count = user_reviews.count()

    except Exception as e:
        print(e)
        return render(request, '404.html')

    return render(request, 'accounts/profile.html', {
        "profile_user": profile_user ,
        "user_reviews": user_reviews,
        "review_count": review_count

    })


def update_user_profile(request: HttpRequest):

    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile", "alert-warning")
        return redirect("accounts:sign_in")

    if request.method == "POST":
        try:
            with transaction.atomic():

                user: User = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile: UserProfile = user.userprofile

                profile.bio = request.POST["bio"]
                profile.website = request.POST["website"]

                if "profile_picture" in request.FILES:
                    profile.profile_picture = request.FILES["profile_picture"]

                profile.save()

                messages.success(request, "Updated profile successfully", "alert-success")

        except Exception as e:
            messages.error(request, "Couldn't update profile", "alert-danger")
            print(e)

    return render(request, "accounts/update_profile.html")
