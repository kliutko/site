
from django.urls import path, include
from modules.system.views import IndexListView, FeedbackCreateView, AboutListView, FaqListView, ConfListView, \
    RulesListView, ReklamaInfoListView
from modules.blog.views import ArticleListView, ArticleDetailView


app_name = 'system'

urlpatterns = [
    path('', IndexListView.as_view(), name='home'),
    # path('blog/', ArticleListView.as_view(), name='blog'),
    # path('articles/<str:slug>/', ArticleDetailView.as_view(), name='articles_detail'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('faq/', FaqListView.as_view(), name='faq'),
    path('сonf/', ConfListView.as_view(), name='сonf'),
    path('rules/', RulesListView.as_view(), name='rules'),
    path('reklamainfo/', ReklamaInfoListView.as_view(), name='reklamainfo'),

    path('page/<str:slug>/', AboutListView.as_view(), name='about'),

]