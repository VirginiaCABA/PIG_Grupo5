from django import template
from datetime import datetime

register = template.Library()

@register.filter
def format_date(value):
    #format_string="%d-%m-%Y %H:%M:%S"
    format_string="%Y-%m-%d"
    if value:
        if isinstance(value, str):
            value = datetime.strptime(value, format_string)
        return value.strftime(format_string)
    return ""


