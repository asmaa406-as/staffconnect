from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/new/', views.PostCreateView.as_view(), name='create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='delete'),
]
