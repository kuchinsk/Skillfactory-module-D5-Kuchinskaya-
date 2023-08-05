from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.paginator import Paginator  # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin  # миксин, проверка наличия аутентификации пользователя

from .filters import PostFilter
from .forms import PostForm
from .models import Post


class News(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-timePost')
    paginate_by = 10


class PostList(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class Search(ListView):
    model = Post
    template_name = 'search.html'
    queryset = Post.objects.order_by('-timePost')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = 'news.add_Post'


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm
    permission_required = 'news.change_Post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news:post_list')


class AddProduct(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
