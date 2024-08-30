# Generated by Django 5.0.8 on 2024-08-30 17:06

import django.core.validators
import django.db.models.deletion
import django_ckeditor_5.fields
import mptt.fields
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название категории')),
                ('slug', models.SlugField(blank=True, max_length=255, verbose_name='URL категории')),
                ('description', models.TextField(verbose_name='Описани категории')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='news.newscategory', verbose_name='Родительская категория')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'db_table': 'news_categories',
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True, verbose_name='URL')),
                ('description', django_ckeditor_5.fields.CKEditor5Field(verbose_name='Описание')),
                ('thumbnail', models.ImageField(blank=True, upload_to='images/news/thumbnails/blog/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='превью новости')),
                ('status', models.CharField(choices=[('published', 'Опубликовано'), ('draft', 'Черновик')], default='published', max_length=20, verbose_name='Статус новости')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('fixed', models.BooleanField(default=False, verbose_name='Зафиксировано')),
                ('author', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='author_news', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updater_news', to=settings.AUTH_USER_MODEL, verbose_name='Обновил')),
                ('category', mptt.fields.TreeManyToManyField(related_name='articles', to='news.newscategory', verbose_name='Категории')),
            ],
            options={
                'verbose_name': 'Статья',
                'verbose_name_plural': 'Статьи',
                'db_table': 'news_articles',
                'ordering': ['-fixed', '-time_create'],
            },
        ),
        migrations.CreateModel(
            name='NewsComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=3000, verbose_name='Текст комментария')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Время обновления')),
                ('status', models.CharField(choices=[('published', 'Опубликовано'), ('draft', 'Черновик')], default='published', max_length=10, verbose_name='Статус новости')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_comments', to='news.newsarticle', verbose_name='Новость')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_comments_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news_children', to='news.newscomment', verbose_name='Родительский комментарий')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'news_comments',
                'ordering': ['-time_create'],
            },
        ),
        migrations.CreateModel(
            name='NewsRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Нравится'), (-1, 'Не нравится')], verbose_name='Значение')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP Адрес')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_ratings', to='news.newsarticle', verbose_name='Новость')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Рейтинг',
                'verbose_name_plural': 'Рейтинги',
                'ordering': ('-time_create',),
            },
        ),
        migrations.CreateModel(
            name='NewsViewCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='IP адрес')),
                ('viewed_on', models.DateTimeField(auto_now_add=True, verbose_name='Дата просмотра')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='news_views', to='news.newsarticle')),
            ],
            options={
                'verbose_name': 'Просмотр',
                'verbose_name_plural': 'Просмотры',
                'ordering': ('-viewed_on',),
            },
        ),
        migrations.AddIndex(
            model_name='newsarticle',
            index=models.Index(fields=['-fixed', '-time_create', 'status'], name='news_articl_fixed_990ad8_idx'),
        ),
        migrations.AddIndex(
            model_name='newscomment',
            index=models.Index(fields=['-time_create', 'time_update', 'status', 'parent'], name='news_commen_time_cr_c953b9_idx'),
        ),
        migrations.AddIndex(
            model_name='newsrating',
            index=models.Index(fields=['-time_create', 'value'], name='news_newsra_time_cr_aa4410_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='newsrating',
            unique_together={('article', 'ip_address')},
        ),
        migrations.AddIndex(
            model_name='newsviewcount',
            index=models.Index(fields=['-viewed_on'], name='news_newsvi_viewed__d9dc5a_idx'),
        ),
    ]
