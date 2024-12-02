from django.contrib import admin

from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username',)
    ordering = ('username',)
    exclude = ('password', 'is_superuser', 'groups', 'user_permissions')
