from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from authManager.forms import RegisterForm, LoginForm
from authManager.models import CustomUser


def register(request):
    if request.method == "GET":
        return render(request, "auth/register.html", {"user_form": RegisterForm()})

    if request.method == "POST":
        form = RegisterForm(request.POST)

        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            username_taken = CustomUser.objects.filter(username=username).exists()
            email_taken = CustomUser.objects.filter(email=email).exists()

            if username_taken:
                error = "Selected username is already taken."
            if email_taken:
                error = "User with that email already exists."

            if not username_taken and not email_taken:
                try:
                    validate_password(password1)
                except ValidationError as e:
                    return render(request, "auth/register.html",
                                  {'password_errors': e.messages, 'user_form': RegisterForm()})
                else:
                    if form.is_valid():
                        user = form.save(commit=False)
                        user.first_name = form.cleaned_data['first_name']
                        user.last_name = form.cleaned_data['last_name']
                        user.save()

                        user = authenticate(username=username, password=password1)
                        login(request, user)
                    return redirect("shop")

        else:
            error = "Passwords do not match. Please type them again."

        return render(request, "auth/register.html", {"user_form": RegisterForm(), "error": error})


def login_user(request):
    if request.method == "GET":
        return render(request, "auth/login_page.html", {"form": LoginForm()})

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("shop")
        else:
            user_exists = CustomUser.objects.filter(username=username).exists()
            if user_exists:
                error = "Incorrect password."
            else:
                error = f"User {username} already exists."
            return render(request, "auth/login_page.html", {"form": LoginForm(), "error": error})

@login_required()
def logout_user(request):
    logout(request)
    return render(request, "basket/shop.html")