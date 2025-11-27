from django import template

register = template.Library()

@register.filter
def lookup(dictionary, key):
    """Custom template filter to get dictionary value by key"""
    return dictionary.get(key, [])
