from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost

class BlogListView(ListView):
    """Список опубликованных блоговых записей"""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Фильтрация: только статьи с положительным признаком публикации"""
        queryset = super().get_queryset()
        return queryset.filter(is_published=True)

class BlogDetailView(DetailView):
    """Детальный просмотр статьи со встроенным счетчиком"""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Счетчик просмотров увеличивается при каждом открытии статьи"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj

class BlogCreateView(CreateView):
    """Создание новой статьи"""
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

class BlogUpdateView(UpdateView):
    """Редактирование статьи с умным редиректом"""
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        """После редактирования перенаправляем на страницу этой же статьи"""
        return reverse('blog:detail', kwargs={'pk': self.object.pk})

class BlogDeleteView(DeleteView):
    """Удаление блоговой записи"""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    