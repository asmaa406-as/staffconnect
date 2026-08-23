from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """HR-facing admin config for announcements."""

    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'body', 'author__username']
    list_filter = ['author', 'created_at']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
