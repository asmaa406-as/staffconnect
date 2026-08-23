import os

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile


class RegisterForm(UserCreationForm):
    """Registration form: username, email, password (+ confirmation)."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self, commit=True):
        # UserCreationForm already hashes the password via set_password
        # internally on save(); we just make sure the email is stored too.
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


def validate_avatar(file):
    """Server-side validation: extension whitelist + max size."""
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in settings.ALLOWED_AVATAR_EXTENSIONS:
        raise forms.ValidationError(
            f'Unsupported file type "{ext}". Allowed: {", ".join(settings.ALLOWED_AVATAR_EXTENSIONS)}'
        )
    max_bytes = settings.MAX_AVATAR_SIZE_MB * 1024 * 1024
    if file.size > max_bytes:
        raise forms.ValidationError(
            f'File too large. Maximum size is {settings.MAX_AVATAR_SIZE_MB}MB.'
        )


class ProfileForm(forms.ModelForm):
    """Edit-profile form: department, bio, avatar upload."""

    class Meta:
        model = Profile
        fields = ['department', 'bio', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        # Only validate newly-uploaded files, not the existing stored one.
        if avatar and hasattr(avatar, 'content_type'):
            validate_avatar(avatar)
        return avatar


class UserUpdateForm(forms.ModelForm):
    """Lets the user update their display name fields alongside the profile."""

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
