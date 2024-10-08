"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from modules.blog.sitemaps import StaticSitemap, ArticleSitemap
from modules.blog.feeds import LatestArticlesFeed
from modules.news.sitemaps import NewsArticleSitemap

sitemaps = {
    'static': StaticSitemap,
    'articles': ArticleSitemap,
    'news': NewsArticleSitemap,
}

handler403 = 'modules.system.views.tr_handler403'
handler404 = 'modules.system.views.tr_handler404'
handler500 = 'modules.system.views.tr_handler500'

urlpatterns = [

    # path('', include('modules.system.urls')),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('feeds/latest/', LatestArticlesFeed(), name='latest_articles_feed'),
    path('users/', include('modules.users.urls')),
    path('blog/', include('modules.blog.urls')),
    path('news/', include('modules.news.urls')),
    path('system/', include('modules.system.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)