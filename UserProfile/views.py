import locale
from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpRequest


from .models import UserProfile, Action, Position, Subject
from .forms import UserForm, UserFormEdit, SignInForm, ActionForm, SubjectForm, PositionForm, UserProfileForm
from TaskManager.models import Schedule


locale.setlocale(locale.LC_TIME, 'uk_UA.UTF-8')


def sign_up(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)  # одразу логін
            messages.success(request, "Реєстрація пройшла успішно!")
            return redirect("index")
        else:
            messages.error(request, "Будь ласка, виправте помилки у формі.")
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "sign_up.html", {
        "sign_up_form": user_form,
        "profile_form": profile_form
    })


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("index")

    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            if user:
                login(request, user)
                messages.success(request, f"Вітаємо, {user.username}!")
                return redirect("index")
            else:
                messages.error(request, "Невірний логін або пароль")
    else:
        form = SignInForm()

    return render(request, "sign_in.html", {"form": form})


@login_required
def update_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserFormEdit(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Дані оновлено")
            return redirect("profile")
    else:
        user_form = UserFormEdit(instance=user)
        profile_form = UserProfileForm(instance=profile)

    return render(request, "profile.html", {
        "user_form": user_form,
        "profile_form": profile_form
    })


@login_required
def index(request: HttpRequest):
    if User.objects.prefetch_related("UserProfile").prefetch_related("Position") \
        .filter(
            username=request.user.username,
            profile__positions__name__in=["Учень", "Вчитель"]
        ).exists():

        profile = request.user.profile

        if not profile.classroom:
            return render(request, "index.html")

        class_number = int(profile.classroom.name.split("-")[0])
        day = datetime.now().strftime("%A").title()

        task = Schedule.objects.filter(day=day, study=class_number)
        return render(request, "index.html", {"task": task})

    return render(request, "index.html")


@login_required
def logout_view(request:HttpRequest):
    logout(request)
    messages.success(request,"Ви вийшли із системи")
    return redirect("sign_in")