from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PostForm
from .models import Post


class PostListView(ListView):
    """Paginated home page listing every published announcement."""

    model = Post
    template_name = 'posts/home.html'
    context_object_name = 'posts'
    paginate_by = 6


class PostDetailView(DetailView):
    """Single announcement, looked up by its slug."""

    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    """Only authenticated users may publish a new announcement."""

    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Announcement published.')
        return super().form_valid(form)


class AuthorRequiredMixin(UserPassesTestMixin):
    """Shared ownership check: only the original author can edit/delete."""

    def test_func(self):
        post = self.get_object()
        return post.author_id == self.request.user.id


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Announcement updated.')
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/post_confirm_delete.html'
    success_url = reverse_lazy('posts:home')

    def form_valid(self, form):
        messages.success(self.request, 'Announcement deleted.')
        return super().form_valid(form)
