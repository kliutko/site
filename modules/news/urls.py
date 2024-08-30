
from django.urls import path

from modules.news.views import NewsArticleListView, NewsArticleCreateView, NewsArticleBySignedUser, NewsArticleByUser, \
    NewsArticleUpdateView, NewsArticleDeleteView, NewsArticleDetailView, NewsCommentCreateView, \
    NewsArticleByTagListView, NewsArticleByCategoryListview, NewsArticleSearchResultView, NewsRatingCreateView

app_name = 'news'

urlpatterns = [
    # path('', IndexListView.as_view(), name='home'),
    path('', NewsArticleListView.as_view(), name='blog'),
    path('n/create/', NewsArticleCreateView.as_view(), name='articles_create'),
    path('n/signed/', NewsArticleBySignedUser.as_view(), name='articles_by_signed_user'),
    path('n/byusers/', NewsArticleByUser.as_view(), name='articles_by_user'),

    path('n/<str:slug>/update/', NewsArticleUpdateView.as_view(), name='articles_update'),
    path('n/<str:slug>/delete/', NewsArticleDeleteView.as_view(), name='articles_delete'),
    path('n/<str:slug>/', NewsArticleDetailView.as_view(), name='articles_detail'),
    path('n/<int:pk>/comments/create/', NewsCommentCreateView.as_view(), name='comment_create_view'),
    path('n/tags/<str:tag>/', NewsArticleByTagListView.as_view(), name='articles_by_tags'),
    path('category/<str:slug>/', NewsArticleByCategoryListview.as_view(), name='articles_by_category'),
    path('search/', NewsArticleSearchResultView.as_view(), name='search'),
    path('rating/', NewsRatingCreateView.as_view(), name='rating'),

]