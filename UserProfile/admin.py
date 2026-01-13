from django.contrib import admin

from .models import Action, Position, Subject, UserProfile


admin.site.register([Action, Position, Subject, UserProfile])