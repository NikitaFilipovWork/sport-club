from django.contrib import admin

from club.models import Coach, Gym, Athlete, TrainingSession

admin.register(Coach)
admin.register(Gym)
admin.register(Athlete)
admin.register(TrainingSession)
