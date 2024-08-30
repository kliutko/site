from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import NewsViewCount, NewsRating, NewsArticle, NewsCategory
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import NewsComment

# Register your models here.



class NewsCategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
    # )

class NewsArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
    # )


admin.site.register(NewsArticle, NewsArticleAdmin)
admin.site.register(NewsCategory, NewsCategoryAdmin)

@admin.register(NewsComment)
class NewsCommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'time_create', 'status')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)




@admin.register(NewsViewCount)
class NewsViewCountAdmin(admin.ModelAdmin):
    pass

@admin.register(NewsRating)
class NewsRatingAdmin(admin.ModelAdmin):
    pass
# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}