# custom_filters.py

from django import template
from django.utils.timesince import timesince
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def humanize_time(timestamp):
    now = localtime()
    delta = now - timestamp

    if delta.days > 0:
        return timestamp.strftime('%b %d, %Y')  # Format as date
    elif delta.seconds < 60:
        return 'just now'
    elif delta.seconds < 3600:
        minutes = delta.seconds // 60
        return f'{minutes} minute{"s" if minutes != 1 else ""} ago'
    else:
        hours = delta.seconds // 3600
        return f'{hours} hour{"s" if hours != 1 else ""} ago'


@register.filter
def get_file_extension(url):
    return url.split('.')[-1].lower()