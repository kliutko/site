from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Article
from django_mptt_admin.admin import DjangoMpttAdmin
# Register your models here.



class CategoryAdmin(DjangoMpttAdmin):
    prepopulated_fields = {"slug": ("title",)}
    # list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
    # list_display_links = ('title', 'slug')
    # fieldsets = (
    #     ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
    #     ('Описание', {'fields': ('description',)})
    # )


admin.site.register(Category, CategoryAdmin)

# @admin.register(Category)
# class CategoryAdmin(DraggableMPTTAdmin):
#     """
#     Админ панель модели категорий
#     """
#     list_display = ('tree_actions', 'indented_title', 'id', 'title', 'slug')
#     list_display_links = ('title', 'slug')
#     prepopulated_fields = {'slug': ('title',)}
#
#     fieldsets = (
#         ('Основная информация', {'fields': ('title', 'slug', 'parent',)}),
#         ('Описание', {'fields': ('description',)})
#     )

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}