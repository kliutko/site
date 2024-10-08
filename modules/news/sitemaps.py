from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import NewsArticle


class NewsArticleSitemap(Sitemap):
    """
    Карта-сайта для статей
    """

    changefreq = 'monthly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return NewsArticle.objects.all()

    def lastmod(self, obj):
        return obj.time_update


class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц
    """

    def items(self):
        return ['system:feedback',]

    def location(self, item):
        return reverse(item)