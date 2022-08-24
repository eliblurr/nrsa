from django import template
from wagtail.core.models import Page, Site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nsra.executive.models import Executive

register = template.Library()

@register.inclusion_tag('tags/executive.html', takes_context=True)
def get_executives(context):
    page = context['request'].GET.get('page')
    qs = Executive.objects.filter(featured=True).all()
    
    paginator = Paginator(qs, 4) 
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    
    return {
        'executives': qs,
        'request': context['request'],
    }
