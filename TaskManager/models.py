from django.db import models

from Resource.models import Resource
from UserProfile.models import Subject


class Schedule(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, blank=True, verbose_name="Кабінет")
    meet_url = models.URLField(verbose_name="Посилання на урок", max_length=1000, default=None, blank=True)
    day = models.CharField(max_length=100, verbose_name="День тижня")
    number = models.PositiveIntegerField(verbose_name="Номер занятть")
    study = models.PositiveIntegerField("Класс")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Предмет")

    def __str__(self):
        return f"{self.subject} на {self.number} уроці {self.study} клас"