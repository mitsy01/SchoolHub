from django.urls import path

from . import views
from Booking.urls import urlpatterns

urlpatterns =[
    path("", views.schedule_view, name="schedule_view"),
    path("filtered/", views.schedule_view_filtered, name="schedule_view_filtered"),
    path("add/", views.add_schedule, name="add_schedule"),
    path("update/<int:id>/", views.update_schedule, name="update_schedule"),
    path("delete/<int:id>", views.delete_schedule, name="delete_schedule")
]