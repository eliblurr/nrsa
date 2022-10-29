from django import template
from wagtail.core.models import Page, Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nsra.executive.models import Executive

register = template.Library()

@register.inclusion_tag('tags/executive.html', takes_context=True)
def get_executives(context):
    return context
