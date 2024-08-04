from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView
from .models import Article, Category
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from ..services.mixins import AuthorRequiredMixin
from modules.blog.forms import ArticleCreateForm, ArticleUpdateForm


# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    allow_empty = False
    paginate_by = 2
    paginate_orphans = 0
    paginator_class = Paginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог>'
        return context

class ArticleDetailView(DeleteView):
    model = Article
    template_name = 'blog/articles_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context


class ArticleByCategoryListview(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    category = None
    allow_empty = False
    paginate_by = 2
    paginate_orphans = 0
    paginator_class = Paginator

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        queryset = Article.objects.all().filter(category__slug=self.category.slug )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Статьи из категории: {self.category.title}'
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'blog/articles_create.html'
    form_class = ArticleCreateForm
    login_url = 'blog:home'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class ArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Article
    template_name = 'blog/articles_update.html'
    context_object_name = 'article'
    form_class = ArticleUpdateForm
    login_url = 'blog:home'
    success_message = 'Материал был успешно обновлен'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)

class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('blog:home')
    context_object_name = 'article'
    template_name = 'blog/articles_delete.html'
    # queryset = model.objects.detail()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'
        return context