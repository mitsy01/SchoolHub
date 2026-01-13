from django.contrib import admin

from .models import Location, Resource


admin.site.register([Location, Resource])
