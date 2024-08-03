
from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleByCategoryListview


app_name = 'blog'

urlpatterns = [
    # path('', IndexListView.as_view(), name='home'),
    path('', ArticleListView.as_view(), name='blog'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('category/<str:slug>/', ArticleByCategoryListview.as_view(), name='articles_by_category'),
]