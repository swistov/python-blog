from django import template
from news.models import Categories

register = template.Library()


@register.simple_tag(name='get_list_categories')
def get_categories():
    return Categories.objects.all()


@register.inclusion_tag('news/list_categories.html')
def show_categories():
    categories = Categories.objects.all()
    return {'categories': categories}
