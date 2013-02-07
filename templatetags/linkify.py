from django.template import Library
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

register = Library()

@register.filter
def linkify(value):
    value = escape(value)
    value = re.sub(r'(https?://[-a-zA-Z0-9._/&%=?]+)', r'<a href="\1">\1</a>', value)
    value = re.sub(r'([-a-zA-Z0-9_.+]+@[-a-zA-Z0-9.]+)', r'<a href="mailto:\1">\1</a>', value)
    return mark_safe(value)
