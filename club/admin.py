from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from club.models import Gym, TrainingSession, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = BaseUserAdmin.list_display + ("role",)
    list_filter = BaseUserAdmin.list_filter + ("role",)
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Club info", {"fields": ("role", "birth_date", "weight", "coaches")}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Club info", {"fields": ("first_name", "last_name", "role")}),
    )


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    pass


@admin.register(TrainingSession)
class TrainingSessionAdmin(admin.ModelAdmin):
    pass
