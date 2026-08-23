from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Extends Django's built-in User with the extra fields NovaTech needs:
    department, a short bio, and a profile photo.
    One-to-one so every User has exactly one Profile.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text='JPG, PNG or WEBP, max 2MB.',
    )

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def avatar_url(self):
        """Return the uploaded avatar URL, or a default placeholder."""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/img/default-avatar.png'
