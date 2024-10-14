from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.urls import reverse
from modules.services.utils import unique_slugify
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from modules.services.utils import unique_slugify, image_compress
from datetime import date
# Create your models here.

User = get_user_model()


class Category(MPTTModel):
    """
    Модель категорий с вложеностью
    pip install django-mptt для вложенных категорий
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описани категории',)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория',
    )

    class MPTTMeta:
        """
        Сортировка по вложенносьти
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица с данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'
        unique_together = [['parent', 'slug']]

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('blog:articles_by_category', kwargs={'slug': self.slug})



class Article(models.Model):
    """
    Модель постов для сайта
    pip install pillow для работы ImageField
    """

    class ArticleManager(models.Manager):
        def all(self):
            return self.get_queryset().select_related('author').prefetch_related('category', 'ratings', 'views').filter(status='published')

        def detail(self):
            """
            Детальная статья (SQL запрос с фильтрацией для страницы со статьёй)
            """
            return self.get_queryset() \
                .select_related('author') \
                .prefetch_related('category', 'comments', 'comments__author', 'comments__author__profile', 'tags','ratings', 'views') \
                .filter(status='published')



    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    description = CKEditor5Field(verbose_name='Описание', config_name='extends')
    thumbnail = models.ImageField(
        verbose_name='превью поста',
        blank=True,
        upload_to='images/thumbnails/blog/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]

    )
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=20)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts', default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True, related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Зафиксировано', default=False)
    category = TreeManyToManyField('Category', related_name='articles', verbose_name='Категории')

    tags = TaggableManager()
    objects = ArticleManager()
    class Meta:
        db_table = 'app_articles'
        ordering = ['-fixed', '-time_create']
        indexes = [models.Index(fields=['-fixed', '-time_create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return f'{self.title}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.thumbnail if self.pk else None

    def get_absolute_url(self):
        return reverse('blog:articles_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)

        if self.__thumbnail != self.thumbnail and self.thumbnail:
            image_compress(self.thumbnail.path, width=500, height=500)

    def get_sum_rating(self):
        return sum([rating.value for rating in self.ratings.all()])

    def get_view_count(self):
        """
        Возвращает количество просмотров для данной статьи
        """
        return self.views.count()

    def get_count_comments(self):
        """
        Возвращает количество просмотров для данной статьи
        """
        return self.comments.count()

    def get_today_view_count(self):
        """
        Возвращает количество просмотров для данной статьи за сегодняшний день
        """
        today = date.today()
        return self.views.filter(viewed_on__date=today).count()


class Comment(MPTTModel):
    """
    Модель древовидных комментариев
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья', related_name='comments')
    # Автор комментария (пользователь) если авторизован
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments_author', null=True, blank=True)
    # Гости сайта, если неавторизованные
    name = models.CharField(max_length=255, verbose_name='Имя посетителя', blank=True)
    email = models.EmailField(max_length=255, verbose_name='Email посетителя', blank=True)
    # Прочие поля
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        order_insertion_by = ('-time_create',)

    class Meta:
        db_table = 'app_comments'
        indexes = [models.Index(fields=['-time_create', 'time_update', 'status', 'parent'])]
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        if self.author:
            return f'{self.author}:{self.content}'
        else:
            return f'{self.name} ({self.email}):{self.content}'

    @property
    def get_avatar(self):
        if self.author:
            return self.author.profile.get_avatar
        return f'https://ui-avatars.com/api/?size=190&background=random&name={self.name}'


class Rating(models.Model):
    """
    Модель рейтинга: Лайк - Дизлайк
    """
    article = models.ForeignKey(to=Article, verbose_name='Статья', on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(to=User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    value = models.IntegerField(verbose_name='Значение', choices=[(1, 'Нравится'), (-1, 'Не нравится')])
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    ip_address = models.GenericIPAddressField(verbose_name='IP Адрес')

    class Meta:
        unique_together = ('article', 'ip_address')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create', 'value'])]
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

    def __str__(self):
        return self.article.title


class ViewCount(models.Model):
    """
    Модель просмотров для статей
    """
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.article.title