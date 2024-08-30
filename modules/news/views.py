from django.db.models.functions import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, UpdateView, DetailView
from .mixins import NewsViewCountMixin
from .models import NewsArticle, NewsRating, NewsCategory
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin

from ..services.mixins import AuthorRequiredMixin
from modules.blog.forms import ArticleCreateForm, ArticleUpdateForm
from django.views.generic import CreateView
from taggit.models import Tag
from .forms import NewsArticleUpdateForm, NewsCommentCreateForm
from .models import NewsComment
import random
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from datetime import date
from django.views.generic import View

from ..services.utils import get_client_ip
from ..system.mixins import ViewCountReklamaMixin
from ..system.models import Reklama
from django.utils import timezone
from ..users.models import Profile
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

now = timezone.localtime()
# now = datetime.datetime.now().time()
# Create your views here.


class NewsArticleListView(ViewCountReklamaMixin, ListView):
    model = NewsArticle
    template_name = 'news/articles_list.html'
    context_object_name = 'articles'
    allow_empty = False
    paginate_by = 10
    paginate_orphans = 0
    paginator_class = Paginator


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог'
        context['banner_header'] = Reklama.objects.all().filter(placement='header_banners_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        context['banner_footer'] = Reklama.objects.all().filter(placement='footer_banners_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        context['left_blog'] = Reklama.objects.all().filter(placement='left_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        context['left_down_blog'] = Reklama.objects.all().filter(placement='left_down_blog', status='inwork', start_time__lte=now, stop_time__gte=now)

        return context

class NewsArticleDetailView(NewsViewCountMixin, DetailView):
    model = NewsArticle
    template_name = 'news/articles_detail.html'
    context_object_name = 'article'
    queryset = model.objects.detail()

    def get_similar_articles(self, obj):
        article_tags_ids = obj.tags.values_list('id', flat=True)
        similar_articles = NewsArticle.objects.filter(tags__in=article_tags_ids).exclude(id=obj.id)
        similar_articles = similar_articles.annotate(related_tags=Count('tags')).order_by('-related_tags')
        similar_articles_list = list(similar_articles.all())
        random.shuffle(similar_articles_list)
        return similar_articles_list[:6]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['form'] = NewsCommentCreateForm
        context['profile'] = Profile.objects.all()
        context['similar_articles'] = self.get_similar_articles(self.object)
        context['banner_header'] = Reklama.objects.all().filter(placement='header_banners_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        context['banner_footer'] = Reklama.objects.all().filter(placement='footer_banners_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        context['left_blog'] = Reklama.objects.all().filter(placement='left_blog', status='inwork', start_time__lte=now, stop_time__gte=now)
        context['left_down_blog'] = Reklama.objects.all().filter(placement='left_down_blog', status='inwork', start_time__lte=now, stop_time__gte=now)

        return context




class NewsRatingCreateView(View):
    model = NewsRating

    def post(self, request, *args, **kwargs):
        article_id = request.POST.get('article_id')
        value = int(request.POST.get('value'))
        ip_address = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        rating, created = self.model.objects.get_or_create(
            article_id=article_id,
            ip_address=ip_address,
            defaults={'value': value, 'user': user},
        )

        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({'status': 'deleted', 'rating_sum': rating.article.get_sum_rating()})
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({'status': 'updated', 'rating_sum': rating.article.get_sum_rating()})
        return JsonResponse({'status': 'created', 'rating_sum': rating.article.get_sum_rating()})





class NewsArticleSearchResultView(ListView):
    """
    Реализация поиска статей на сайте
    """
    model = NewsArticle
    context_object_name = 'articles'
    paginate_by = 10
    allow_empty = True
    template_name = 'news/articles_list.html'

    def get_queryset(self):
        query = self.request.GET.get('do')
        search_vector = SearchVector('description', weight='B') + SearchVector('title', weight='A')
        search_query = SearchQuery(query)
        return (self.model.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.3).order_by('-rank'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результаты поиска: {self.request.GET.get("do")}'
        return context

class NewsArticleByTagListView(ListView):
    model = NewsArticle
    template_name = 'news/articles_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    tag = None

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag'])
        queryset = NewsArticle.objects.all().filter(tags__slug=self.tag.slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Новости по тегу: {self.tag.name}'
        return context


class NewsArticleByCategoryListview(ListView):
    model = NewsArticle
    template_name = 'news/articles_list.html'
    context_object_name = 'articles'
    category = None
    allow_empty = False
    paginate_by = 2
    paginate_orphans = 0
    paginator_class = Paginator

    def get_queryset(self):
        self.category = NewsCategory.objects.get(slug=self.kwargs['slug'])
        queryset = NewsArticle.objects.all().filter(category__slug=self.category.slug )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Новости из категории: {self.category.title}'
        return context



class NewsArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = NewsArticle
    template_name = 'news/articles_create.html'
    form_class = ArticleCreateForm
    login_url = 'news:blog'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление новости на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

class NewsArticleUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = NewsArticle
    template_name = 'news/articles_update.html'
    context_object_name = 'article'
    form_class = NewsArticleUpdateForm
    login_url = 'news:blog'
    success_message = 'Материал был успешно обновлен'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление статьи: {self.object.title}'
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)

class NewsArticleDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = NewsArticle
    success_url = reverse_lazy('news:blog')
    context_object_name = 'article'
    template_name = 'news/articles_delete.html'
    # queryset = model.objects.detail()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление статьи: {self.object.title}'

        return context


class NewsCommentCreateView(CreateView):
    model = NewsComment
    form_class = NewsCommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_valid(self, form):
        news_comments = form.save(commit=False)
        news_comments.article_id = self.kwargs.get('pk')

        if self.request.user.is_authenticated:
            news_comments.author = self.request.user
            news_comments.name = self.request.user.username
            news_comments.email = self.request.user.email
        else:
            news_comments.name = form.cleaned_data.get('name')
            news_comments.email = form.cleaned_data.get('email')

        news_comments.parent_id = form.cleaned_data.get('parent')
        news_comments.save()

        if self.is_ajax():
            if self.request.user.is_authenticated:
                data = {
                    'is_child': news_comments.is_child_node(),
                    'id': news_comments.id,
                    'author': news_comments.author.username,
                    'parent_id': news_comments.parent_id,
                    'time_create': news_comments.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                    'avatar': news_comments.get_avatar,
                    'content': news_comments.content,
                    'get_absolute_url': news_comments.author.profile.get_absolute_url()
                }
            else:
                data = {
                    'is_child': news_comments.is_child_node(),
                    'id': news_comments.id,
                    'author': news_comments.name,
                    'parent_id': news_comments.parent_id,
                    'time_create': news_comments.time_create.strftime('%Y-%b-%d %H:%M:%S'),
                    'avatar': news_comments.get_avatar,
                    'content': news_comments.content,
                    'get_absolute_url': f'mailto:{news_comments.email}'
                }
            return JsonResponse(data, status=200)

        return redirect(news_comments.article.get_absolute_url())




class NewsArticleBySignedUser(LoginRequiredMixin, ListView):
    """
    Представление, выводящее список статей авторов, на которые подписан текущий пользователь
    """
    model = NewsArticle
    template_name = 'news/articles_list.html'
    context_object_name = 'articles'
    login_url = 'login'
    paginate_by = 10

    def get_queryset(self):
        authors = self.request.user.profile.following.values_list('id', flat=True)
        queryset = self.model.objects.all().filter(author__id__in=authors)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новости авторов'
        return context


class NewsArticleByUser(LoginRequiredMixin, ListView):
    """
    Представление, выводящее список статей авторов, на которые подписан текущий пользователь
    """
    model = NewsArticle
    template_name = 'news/articles_list.html'
    context_object_name = 'articles'
    login_url = 'login'
    paginate_by = 10

    def get_queryset(self):

        queryset = self.model.objects.all().filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои новости'
        return context