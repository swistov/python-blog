from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Rubric, Article


@admin.register(Rubric)
class RubricAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    list_display = ('tree_actions', 'indented_title')
    list_display_links = ('indented_title',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
