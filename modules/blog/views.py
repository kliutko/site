from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from .models import Article, Category
from django.core.paginator import Paginator
# Create your views here.


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/articles_list.html'
    context_object_name = 'articles'
    allow_empty = False
    paginate_by = 2
    paginate_orphans = 0
    paginator_class = Paginator
    # queryset = Article.custom.all()
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