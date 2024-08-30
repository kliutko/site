# Generated by Django 5.0.8 on 2024-08-30 14:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_url_facebook_profile_url_google_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image_header',
            field=models.ImageField(blank=True, default='images/avatars/default.png', upload_to='images/image_head/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], verbose_name='Шапка профиля'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='static/images/avatars/default.png', upload_to='images/avatars/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], verbose_name='Аватар'),
        ),
    ]
