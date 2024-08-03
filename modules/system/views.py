from django.shortcuts import render
from django.views.generic import ListView, DeleteView
from modules.blog.models import Article, Category


# Create your views here.

class IndexListView(ListView):
    model = Article
    # template_name = 'blog/articles_list.html'
    template_name = 'index.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

