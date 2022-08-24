from django import template
from django.core.files.storage import default_storage
import math

register = template.Library()

@register.filter
def image_path(image):
    return image.file.url

@register.filter
def bytes_to_m_bytes(size):
    return str(round(size/1000000, 1)) + 'MB'

@register.filter
def to_list(val):
    return list(val)

@register.filter
def content_type_name(val):
    return val.name.replace('_', ' ')
