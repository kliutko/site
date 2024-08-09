
from django.urls import path
from .views import IndexListView, FeedbackCreateView
from modules.blog.views import ArticleListView, ArticleDetailView


app_name = 'system'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    # path('blog/', ArticleListView.as_view(), name='blog'),
    # path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
]