from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Article
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Comment

# Register your models here.



class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
    # )

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
    # )


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)

@admin.register(Comment)
class CommentAdminPage(DraggableMPTTAdmin):
    """
    Админ-панель модели комментариев
    """
    list_display = ('tree_actions', 'indented_title', 'article', 'author', 'time_create', 'status')
    mptt_level_indent = 2
    list_display_links = ('article',)
    list_filter = ('time_create', 'time_update', 'author')
    list_editable = ('status',)

# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     prepopulated_fields = {'slug': ('title',)}