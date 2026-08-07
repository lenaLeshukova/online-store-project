from django.urls import path
from blog.views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('blogs/', BlogListView.as_view(), name='list'),
    path('blogs/create/', BlogCreateView.as_view(), name='create'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='detail'),
    path('blogs/<int:pk>/update/', BlogUpdateView.as_view(), name='update'),
    path('blogs/<int:pk>/delete/', BlogDeleteView.as_view(), name='delete'),
]
