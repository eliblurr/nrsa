from .models import ResearchPage, PublicationPage, ResearchCategory, PublicationCategory, ResearchPublicationIndexPage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.http import request, JsonResponse
from django.core import serializers
import json, datetime

def get_page(qs, page=1, size=12):
    paginator = Paginator(qs, size)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages

def get_parent(id):
    return ResearchPublicationIndexPage.objects.get(pk=id)

@csrf_exempt
def get_research(request, parent, category=0, sort='descending', page=1):

    category = int(category)
    sorting = '-first_published_at' if sort=='descending' else 'first_published_at'
    research = ResearchPage.objects.filter().live().descendant_of(get_parent(parent)).order_by(sorting)
    if category:
        research = ResearchCategory.objects.get(pk=category).research.live().descendant_of(get_parent(parent)).order_by(sorting)
    page = get_page(research, page, ResearchPublicationIndexPage.research_pg_size)

    data = {
        'number': page.number,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'objects':[
            {
                'url':obj.url,
                'headline': obj.headline,
                'image':  obj.main_image().get_rendition('original').url if obj.main_image() else "",
            } for obj in page
        ]
    }

    return JsonResponse({"data": data})

@csrf_exempt
def get_publication(request, parent, category=0, sort='descending', page=1):
    
    category = int(category)
    sorting = '-first_published_at' if sort=='descending' else 'first_published_at'
    publications = PublicationPage.objects.filter().live().descendant_of(get_parent(parent)).order_by(sorting)
    if category:
        publications = PublicationCategory.objects.get(pk=category).research.live().descendant_of(get_parent(parent)).order_by(sorting)
    page = get_page(publications, page, ResearchPublicationIndexPage.publication_pg_size)
    
    data = {
        'number': page.number,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'objects':[
            {
                'url':obj.url,
                'headline': obj.headline,
                'image':  obj.main_image().get_rendition('original').url if obj.main_image() else "",
            } for obj in page
        ]
    }

    return JsonResponse({"data": data})
