from django import template
from itertools import groupby
from operator import attrgetter

register = template.Library()

@register.filter
def groupby(queryset, field_name):
    """Mengelompokkan queryset berdasarkan field tertentu"""
    sorted_queryset = sorted(queryset, key=attrgetter(field_name))
    grouped_queryset = {key: list(group) for key, group in groupby(sorted_queryset, key=attrgetter(field_name))}
    return grouped_queryset.items()
