from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, UserLoginForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from userauths.models import Profile, User
import logging

logger = logging.getLogger(__name__)


def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            try:
                new_user = form.save()
                username = form.cleaned_data.get("username")
                messages.success(
                    request, f"Hey {username}, Your account was created successfully."
                )

                # Authenticate user
                new_user = authenticate(
                    request,
                    username=form.cleaned_data["email"],
                    password=form.cleaned_data["password1"],
                )

                if new_user is not None:
                    login(request, new_user)
                    next_url = request.GET.get("next", "core:index")
                    return redirect(next_url)
                else:
                    messages.error(
                        request, "Authentication failed. Please try logging in."
                    )
                    return redirect("userauths:sign-in")

            except Exception as e:
                logger.error(f"Registration error: {str(e)}", exc_info=True)
                messages.error(request, f"Registration failed: {str(e)}")
                # Не возвращаем ошибку, показываем форму снова
        else:
            # Показываем ошибки валидации формы
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "Hey you are already logged in.")
        return redirect("core:index")

    if request.method == "POST":
        try:
            form = UserLoginForm(data=request.POST, request=request)
            if form.is_valid():
                user = form.get_user()
                if user is not None:
                    login(request, user)
                    messages.success(request, "You are logged in.")
                    next_url = request.GET.get("next", "core:index")
                    return redirect(next_url)
                else:
                    messages.error(request, "Invalid credentials. Please try again.")
            else:
                # Показываем ошибки валидации
                for field, errors in form.errors.items():
                    for error in errors:
                        if field == "__all__":
                            messages.error(request, error)
                        else:
                            messages.error(request, f"{field}: {error}")
        except Exception as e:
            logger.error(f"Login error: {str(e)}", exc_info=True)
            messages.error(request, "Login failed. Please try again.")
    else:
        form = UserLoginForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):

    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile-edit.html", context)
