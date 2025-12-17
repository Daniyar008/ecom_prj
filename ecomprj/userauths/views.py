from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm, UserLoginForm, ProfileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.utils.translation import gettext as _
from django.conf import settings
from userauths.models import Profile, User


# User = settings.AUTH_USER_MODEL


def register_view(request):

    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Hey {username}, You account was created successfully."
            )
            new_user = authenticate(
                request,
                username=form.cleaned_data["email"],
                password=form.cleaned_data["password1"],
            )
            login(request, new_user)

            next_url = request.GET.get("next", "core:index")
            return redirect(next_url)
    else:
        form = UserRegisterForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-up.html", context)


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, _("Hey you are already Logged In."))
        return redirect("core:index")

    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _("You are logged in."))
            next_url = request.GET.get("next", "core:index")
            return redirect(next_url)
    else:
        form = UserLoginForm()

    context = {
        "form": form,
    }
    return render(request, "userauths/sign-in.html", context)


def logout_view(request):

    logout(request)
    messages.success(request, _("You logged out."))
    return redirect("userauths:sign-in")


def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, _("Profile Updated Successfully."))
            return redirect("core:dashboard")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "userauths/profile-edit.html", context)
