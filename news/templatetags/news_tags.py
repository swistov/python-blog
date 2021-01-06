from django import template
from django.db.models import Count

from news.models import Categories

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Categories.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = Categories.objects.filter(news__is_published=True).annotate(cnt=Count('news')).filter(cnt__gt=0)
    return {'categories': categories}
