from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import ActivityCategory, ActivityIndexPage
from django.views.decorators.csrf import csrf_exempt
from django.http import request, JsonResponse
from rest_framework.response import Response
from django.core import serializers

import json 

def get_page(qs, page=1, size=12):
    paginator = Paginator(qs, size)
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)
    return pages

@csrf_exempt
def categorized_page(request, category=None, page=1):

    activities = ActivityCategory.objects.get(pk=category).activities.live() 
    page = get_page(activities, page, ActivityIndexPage.gp_pg_size)

    data = {
        'number': page.number,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'activities':[
            {
                'url':obj.url,
                'headline': obj.headline,
                # 'summary_title': obj.summary_title
                'summary': '',
                'image': obj.main_image().get_rendition('original').url if obj.main_image() else '',
            } for obj in page
        ]
    }

    return JsonResponse({"data": data})

    # 'count', 'end_index', 'has_next', 'has_other_pages', 'has_previous', 'index', 'next_page_number', 'number', 'object_list', 'paginator', 'previous_page_number', 'start_index'
    # image.get_rendition('original')
    # image.get_rendition('fill-320x200')
    # https://groups.google.com/g/wagtail/c/AAARvKmZ8S4