from django import template
from datetime import datetime

register = template.Library()

@register.filter
def month_year(date):
    """Returns month and year from a date object"""
    if not date:
        return ''
    return date.strftime("%B %Y")

@register.filter
def month_year_short(date):
    """Returns abbreviated month and year from a date object"""
    if not date:
        return ''
    return date.strftime("%b %Y")