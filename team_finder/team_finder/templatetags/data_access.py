from django import template

register = template.Library()


@register.filter
def key(dict, k):
    return dict.get(k)
