from django.contrib import admin

from apps.users.models import User


# admin.register(User) is a parameterized decorator ==
# admin.site.register(User, UserAdmin).
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Columns shown in the admin list page.
    list_display = ["email", "first_name", "last_name", "role", "is_staff"]
