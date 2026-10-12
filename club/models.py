from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ATHLETE = ("athlete", "Athlete")
        COACH = ("coach", "Coach")

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.ATHLETE,
    )

    birth_date = models.DateField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)

    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        symmetrical=False,
        blank=True,
        related_name="athletes",
        limit_choices_to={"role": Role.COACH},
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    @property
    def is_coach(self) -> bool:
        return self.role == self.Role.COACH

    @property
    def is_athlete(self) -> bool:
        return self.role == self.Role.ATHLETE

    def __str__(self) -> str:
        full_name = self.get_full_name()
        return full_name or self.username


class Gym(models.Model):
    address = models.CharField(max_length=255)
    coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="gyms",
        blank=True,
        limit_choices_to={"role": User.Role.COACH},
    )

    def __str__(self) -> str:
        return self.address


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
        related_name="coached_sessions",
        limit_choices_to={"role": User.Role.COACH},
    )
    athletes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        limit_choices_to={"role": User.Role.ATHLETE},
    )

    class Meta:
        ordering = ["starts_at"]

    def clean(self):
        if self.starts_at > self.ends_at:
            raise ValueError("Training can not end before it begins!")
        if self.coach_id and not self.coach.is_coach:
            raise ValidationError("Only a user with the 'coach' role can conduct a training session.")

    def __str__(self) -> str:
        return (
            f"Training starts at: {self.starts_at} and finishes at: {self.ends_at}. "
            f"Coach is {self.coach}."
        )
