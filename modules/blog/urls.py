
from django.urls import path
from .views import ArticleListView, ArticleDetailView


app_name = 'blog'

urlpatterns = [
    # path('', IndexListView.as_view(), name='home'),
    path('', ArticleListView.as_view(), name='blog'),
    path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
]