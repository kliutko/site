from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from .models import Article
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