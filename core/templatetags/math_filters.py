from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add_counter(counter, increment):
    """Add increment to counter for delay calculations."""
    try:
        return (int(counter) + int(increment)) * 100
    except (ValueError, TypeError):
        return 100