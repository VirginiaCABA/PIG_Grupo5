from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_date(value, format_string="%d-%m-%Y %H:%M:%S"):
    if value:
        if isinstance(value, str):
            value = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
        return value.strftime(format_string)
    return ""


