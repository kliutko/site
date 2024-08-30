from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article

class LatestArticlesFeed(Feed):
    title = "Ваш сайт - последние новости"
    link = "/feeds/"
    description = "Новые новости на моем сайте."

    def items(self):
        return Article.objects.order_by('-time_update')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return reverse('news:articles_detail', args=[item.slug])