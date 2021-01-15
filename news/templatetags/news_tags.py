from django import template
from django.db.models import Count, F
from django.core.cache import cache

from news.models import Categories

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Categories.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    """Cache"""
    # categories = cache.get('categories')
    # if not categories:
    #     categories = Categories.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)
    #     cache.set('categories', categories, 30)
    categories = Categories.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)

    return {'categories': categories}
