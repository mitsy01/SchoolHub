from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST

from .models import Schedule
from .forms import ScheduleForm
from Booking.permissions import  has_permission


@has_permission("RS")
@require_GET
def schedule_view(request: HttpRequest):
    messages.success(request, "Використайте фільтр")
    schedule_all = Schedule.objects.all()
    return render(request, "schedule_view.html", dict(schedule_all=schedule_all))


@has_permission("RS")
@require_POST
def schedule_view_filtered(request):
    schedule = None
    schedule_all = Schedule.objects.all()

    if request.method == "POST":
        day = request.POST.get("day")
        study = request.POST.get("study")

        if day and study:
            schedule = Schedule.objects.filter(day=day, study=study)
        elif day:
            schedule = Schedule.objects.filter(day=day)
        elif study:
            schedule = Schedule.objects.filter(study=study)
        else:
            schedule = Schedule.objects.none()

    return render(request, "schedule_view.html", {
        "schedule": schedule,
        "schedule_all": schedule_all,
    })



@has_permission("CS")
def add_schedule(request: HttpRequest):
    messages.success(request, "Додати новий урок")
    form = ScheduleForm(data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Урок додано")
        return redirect("add_schedule")

    messages.success(request, "Додати новий урок")
    return render(request, "schedule_add.html", dict(form=form))


@has_permission("CS")
def update_schedule(request: HttpRequest, id: int):
    schedule = Schedule.objects.filter(id=id).first()
    if not schedule:
        return  redirect("schedule_view")


    form = ScheduleForm(data=request.POST or None, instance=schedule)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Дані оновлено")
        return redirect("schedule_view")
    messages.success(request, f"Оновлення{schedule}")
    return render(request, "schedule_add.html", dict(form=form))


@has_permission("CS")
def delete_schedule(request: HttpRequest, id:int):
    schedule = Schedule.objects.filter(id=id).first()
    if not schedule:
        messages.error(request, "Такий урок не знайдено")
        return redirect("schedule_view")

    schedule.delete()
    messages.success(request, f"{schedule} видалено")
    return redirect("schedule_view")
