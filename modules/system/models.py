from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from datetime import date


User = get_user_model()


class Feedback(models.Model):
    """
    Модель обратной связи
    """
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=255, verbose_name='Электронный адрес (email)')
    content = models.TextField(verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя', blank=True, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'
        ordering = ['-time_create']
        db_table = 'app_feedback'

    def __str__(self):
        return f'Вам письмо от {self.email}'


class Reklama(models.Model):
    """
    Модель постов рекламы сайта
    pip install pillow для работы ImageField
    """

    class ReklamaManager(models.Manager):
        def all(self):
            return self.get_queryset().select_related('client').prefetch_related('views').filter(
                status='inwork')
        # def all(self):
        #     return self.get_queryset().select_related('title').prefetch_related('views').filter(
        #         status='inwork')


    STATUS_OPTIONS = (
        ('inwork', 'В работе'),
        ('stopped', 'Остановлена')
    )
    PLACEMENT_OPTIONS = (
        ('header_banners_blog', 'Баннер в шапке раздела блог'),
        ('header_banners_news', 'Баннер в шапке раздела новости'),
        ('header_banners_all', 'Баннер в шапке сквозной'),
        ('left_banners_blog', 'Баннер в левом блоке раздела блог'),
        ('left_banners_news', 'Баннер в левом блоке раздела новости'),
        ('left_banners_all', 'Баннер в левом блоке сквозной'),
        ('footer_banners_blog', 'Баннер в низу раздела блог'),
        ('footer_banners_news', 'Баннер в низу раздела новости'),
        ('footer_banners_all', 'Баннер в низу сквозной'),

    )

    title = models.CharField(verbose_name='Название', max_length=255)
    client = models.ForeignKey(to=User, verbose_name='Клиент', on_delete=models.CASCADE, blank=True, related_name='client_reklama')
    urls = models.URLField(verbose_name='URL', max_length=255, blank=True, unique=False)
    description = models.TextField(verbose_name='Описание')
    thumbnail = models.ImageField(
        verbose_name='Изображение',
        blank=False,
        upload_to='images/reklama/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]

    )
    status = models.CharField(choices=STATUS_OPTIONS, default='inwork', verbose_name='Статус рекламы', max_length=20)
    placement = models.CharField(choices=PLACEMENT_OPTIONS, default='', verbose_name='Размещение рекламы', max_length=20)
    start_time = models.DateTimeField(auto_now_add=False, verbose_name='Время начала')
    stop_time = models.DateTimeField(auto_now=False, verbose_name='Время время окончания')




    objects = ReklamaManager()

    class Meta:
        db_table = 'app_reklama'
        ordering = ['-status', 'start_time']
        indexes = [models.Index(fields=['title', '-start_time', '-stop_time', 'status'])]
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'

    def __str__(self):
        return f'{self.title}, Время начала: {self.start_time}, Время окончания: {self.stop_time}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__thumbnail = self.thumbnail if self.pk else None


    def get_view_count(self):
        """
        Возвращает количество просмотров для данной рекламы
        """
        return self.views.count()

    def get_today_view_count(self):
        """
        Возвращает количество просмотров для данной статьи за сегодняшний день
        """
        today = date.today()
        return self.views.filter(viewed_on__date=today).count()

class ViewCount(models.Model):
    """
    Модель просмотров для статей
    """
    reklama = models.ForeignKey('Reklama', on_delete=models.CASCADE, related_name='views')
    ip_address = models.GenericIPAddressField(verbose_name='IP адрес')
    viewed_on = models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        ordering = ('-viewed_on',)
        indexes = [models.Index(fields=['-viewed_on'])]
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'

    def __str__(self):
        return self.article.title