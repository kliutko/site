from django.contrib import admin

from .models import Feedback, Reklama, ViewCount, About, Faq, Conf, Rules, ReklamaInfo


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('email', 'ip_address', 'user')
    list_display_links = ('email', 'ip_address')



@admin.register(Reklama)
class ReklamaAdmin(admin.ModelAdmin):

    list_display = ('title', 'status', 'client', 'placement', 'start_time', 'stop_time')
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
    # )
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):

    list_display = ('title',)
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(Conf)
class ConfAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')

@admin.register(ReklamaInfo)
class ReklamaInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):

    list_display = ('reklama', 'ip_address', 'viewed_on')





# Register your models here.
