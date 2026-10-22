from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from PeopleHub.apps.users.models import User


# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
       ("Contact details", {"fields": ("phone",)}),
    )


    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Contact details", {"fields": ("phone",)}),
    )

    list_display = (
        "username",
        "email",
        "phone",
        "is_staff",
        "is_active",
    )

    search_fields = ("username", "email", "phone")