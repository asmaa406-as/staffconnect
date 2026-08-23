from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """HR-facing admin config for staff profiles."""

    list_display = ['user', 'department', 'has_avatar']
    search_fields = ['user__username', 'user__email', 'department']
    list_filter = ['department']
    fieldsets = (
        ('Account', {'fields': ('user',)}),
        ('Profile details', {'fields': ('department', 'bio', 'avatar')}),
    )

    @admin.display(boolean=True, description='Avatar uploaded')
    def has_avatar(self, obj):
        return bool(obj.avatar)
