from django.urls import include, path
from .views import *

urlpatterns = [
    # path('upcoming-events-data-views/<parent>/<page>/<sort>', get_upcoming_events, name='upcoming_events'),
    path('past-events-data-views/<parent>/<page>/<sort>', get_past_events, name='past_events'),
    # path('events-data-views/<parent>/<page>/<sort>', get_events, name='get_events'),
    path('news-data-views/<parent>/<page>/<sort>', get_news, name='get_news'),
]