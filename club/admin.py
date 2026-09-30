from django.contrib import admin

from club.models import Coach, Gym, Athlete, TrainingSession

admin.site.register(Coach)
admin.site.register(Gym)
admin.site.register(Athlete)
admin.site.register(TrainingSession)
