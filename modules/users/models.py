from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from modules.services.utils import unique_slugify
from django.utils import timezone
from django.core.cache import cache

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    image_header = models.ImageField(
        verbose_name='Шапка профиля',
        upload_to='images/image_head/%Y/%m/%d/',
        default='images/avatars/default.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    following = models.ManyToManyField('self', verbose_name='Подписки', related_name='followers', symmetrical=False, blank=True)
    agree_rules = models.BooleanField(default=False, verbose_name='Согласен с правилами сайта')
    agree_conf = models.BooleanField(default=False, verbose_name='Согласен с политикой конфедициальности')
    url_facebook = models.URLField(verbose_name='Ссылка на Facebook', max_length=255, blank=True, unique=False, help_text='Ссылка должна начинаться с: http:// или https://')
    url_pinterest = models.URLField(verbose_name='Ссылка на Pinterest', max_length=255, blank=True, unique=False, help_text='Ссылка должна начинаться с: http:// или https://')
    url_twitter = models.URLField(verbose_name='Ссылка на Twitter', max_length=255, blank=True, unique=False, help_text='Ссылка должна начинаться с: http:// или https://')
    url_google = models.URLField(verbose_name='Ссылка на Google plus', max_length=255, blank=True, unique=False, help_text='Ссылка должна начинаться с: http:// или https://')
    url_instagram = models.URLField(verbose_name='Ссылка на Instagram', max_length=255, blank=True, unique=False, help_text='Ссылка должна начинаться с: http:// или https://')



    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """
        db_table = 'app_profiles'
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        """
        Сохранение полей модели при их отсутствии заполнения
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('users:profile_detail', kwargs={'slug': self.slug})

    def is_online(self):
        last_seen = cache.get(f'last-seen-{self.user.id}')
        if last_seen is not None and timezone.now() < last_seen + timezone.timedelta(seconds=300):
            return True
        return False

    def get_count_followers(self):
        """
        Возвращает количество
        """
        return self.profile.followers.count()
    def get_count_following(self):
        """
        Возвращает количество
        """
        return self.following.count()

    @property
    def get_avatar(self):
        if self.avatar:
            return f'{self.avatar.url}?300x200'
        return f'https://ui-avatars.com/api/?size=300&background=random&name={self.slug}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()