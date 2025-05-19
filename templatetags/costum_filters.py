from django import template
import base64

register = template.Library()

@register.filter
def b64encode(value):
    """Encode binary data to base64."""
    return base64.b64encode(value).decode('utf-8')