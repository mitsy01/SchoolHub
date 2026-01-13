from django.db import models
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _


class Action(models.Model):
    class ActionChoice(models.TextChoices):
        CREATEBOOKING = "CB", _("CreateBooking")
        READBOOKING = "RB", _("ReadBooking")
        UPDATEBOOKING = "UB", _("UpdateBooking")

    name = models.CharField(
        max_length=100,
        verbose_name="Дозволена дія",
        help_text="Введіть назву дії",
        choices=ActionChoice.choices,
        default=ActionChoice.READBOOKING
    )

    def __str__(self):
        return f"Назва дії: {self.name}"

class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name="Посада", help_text="Введіть посаду")
    action = models.ManyToManyField(Action, verbose_name="Список дозволів", help_text="Оберіть дозвіл")
    
    def __str__(self):
        return f"Посада: {self.name}|Дії: {'.'.join([action.name for action in self.action.all()])}"

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва предмета", help_text="Введіть назву предмета")
    
    def __str__(self):
        return f"Назва предмета: {self.name}"


class ClassRoom(models.Model):
    name = models.CharField(max_length=50, verbose_name="Назва класу")
    description = models.CharField(max_length=256, verbose_name="Опис класу", null=True, blank=True, default=None )
    subjects = models.ManyToManyField(Subject, null=True, blank=True, default=None, verbose_name="Список предметів")

    def __str__(self):
        return f"{self.name} клас "

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    position = models.ManyToManyField(Position, null=True, blank=True, default=None)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, default=None)
    avatar = models.ImageField(upload_to=".", verbose_name="Аватарка", null=True, blank=True, default=None)
    bio = models.TextField(verbose_name="Про себе", null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None, verbose_name="Номер телефону")
    
    def __str__(self):
        return f"Користувач: {self.user.get_full_name()}|{self.classroom}"