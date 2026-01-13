from django.contrib import admin

from .models import Status, Booking, BookingLog, Action


admin.site.register([Status, Booking, BookingLog, Action])
