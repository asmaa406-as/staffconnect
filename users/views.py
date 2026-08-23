from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ProfileForm, RegisterForm, UserUpdateForm
from .models import Profile


def register_view(request):
    """Handle new employee sign-up."""
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Every new user automatically gets an (initially empty) profile.
            Profile.objects.get_or_create(user=user)
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('users:login')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})


class LoginView(DjangoLoginView):
    """Session-based login using Django's AuthenticationForm."""

    template_name = 'users/login.html'
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


@require_POST
@login_required
def logout_view(request):
    """Logout must only ever be triggered via POST, never GET."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('users:login')


@login_required
def profile_view(request):
    """Show the logged-in user's own profile page."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def edit_profile_view(request):
    """Edit the logged-in user's profile: department, bio, avatar."""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
        messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
