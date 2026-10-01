from django.contrib import admin

from club.models import Gym, TrainingSession, User

admin.site.register(User)
admin.site.register(Gym)
admin.site.register(TrainingSession)
