from django.conf import settings
from django.urls import include, path, re_path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from nsra.search import views as search_views
from .api import api_router

from nsra.research_and_publication import urls as research_and_publication_urls
from nsra.newsletter.urls import urlpatterns as newsletter_urlpatterns
from nsra.news_and_events import urls as news_and_events_urls
from nsra.activity import urls as activity_urls
from nsra.stats import urls as stats_urls

from .views import unauthorized

from wagtail.core import views
views.serve.csrf_exempt = True

handler404 = 'nsra.views.handle404'
handler403 = 'nsra.views.handle403'
handler400 = 'nsra.views.handle400'
handler500 = 'nsra.views.handle500'

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    re_path(r'site-search-x01-csd-12', search_views.search, name='search'),
    path('api/v2/', api_router.urls),

    path('mail/', include(newsletter_urlpatterns), name='birdsong'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('statistics/accidents/', include(stats_urls), name='mycharts'),

    path('401/', unauthorized, name='unauthorized'),

    path('', include(activity_urls), name='activity'),
    path('', include(news_and_events_urls), name='news_and_events'),
    path('', include(research_and_publication_urls), name='research_and_publications'),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]


