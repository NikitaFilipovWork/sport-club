from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Coach(AbstractUser):
    pass


class Gym(models.Model):
    address = models.CharField(max_length=255)
    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="gyms"
    )


class Athlete(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    weight = models.FloatField()
    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="athletes"
    )
    gyms = models.ManyToManyField(Gym, related_name="athletes")

    class Meta:
        ordering = ["birth_date"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainingSession(models.Model):
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    gym = models.ForeignKey(Gym, on_delete=models.PROTECT, related_name="sessions")
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="sessions"
    )
    athlete = models.ForeignKey(Athlete, on_delete=models.PROTECT, related_name="sessions")
