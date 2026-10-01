from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Coach(AbstractUser):
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Gym(models.Model):
    address = models.CharField(max_length=255)
    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="gyms"
    )

    def __str__(self) -> str:
        return f"{self.address}"


class Athlete(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    weight = models.FloatField()
    is_active = models.BooleanField(default=True)
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

    gym = models.ForeignKey(
        Gym,
        on_delete=models.PROTECT,
        related_name="sessions",
    )

    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="sessions",
    )

    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.PROTECT,
        related_name="sessions",
    )

    def __str__(self) -> str:
        return (f"Training starts at: {self.starts_at} and finishes at:{self.ends_at}. "
                f"Coach is {self.coach}.")