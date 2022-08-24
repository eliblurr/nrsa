from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import NewsPage, EventPage, NewsEventsIndexPage
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
    return NewsEventsIndexPage.objects.get(pk=id)

@csrf_exempt
def get_news(request, parent, sort='descending', page=1):

    sorting = '-first_published_at' if sort=='descending' else 'first_published_at'
    news = NewsPage.objects.filter().live().descendant_of(get_parent(parent)).order_by(sorting)
    page = get_page(news, page, NewsEventsIndexPage.news_pg_size)

    data = {
        'number': page.number,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'objects':[
            {
                'url':obj.url,
                'headline': obj.headline,
                'image':  obj.main_image().get_rendition('original').url,
                'date': obj.date
            } for obj in page
        ]
    }

    return JsonResponse({"data": data})

@csrf_exempt
def get_past_events(request, parent, sort='descending', page=1):
    sorting = '-first_published_at' if sort=='descending' else 'first_published_at'
    events = EventPage.objects.filter(date_time__lt=datetime.datetime.now()).live().descendant_of(get_parent(parent)).order_by(sorting)
    page = get_page(events, page, NewsEventsIndexPage.past_event_pg_size)
    
    data = {
        'number': page.number,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'objects':[
            {
                'url':obj.url,
                'headline': obj.headline,
                'image':  obj.main_image().get_rendition('original').url,
                'date': obj.date_time
            } for obj in page
        ]
    }

    return JsonResponse({"data": data})
