from django.urls import include, path
from .views import *

urlpatterns = [
    path('categorized-research/<parent>/<page>/<category>/<sort>', get_research, name='categorized_research'),
    path('categorized-publication/<parent>/<page>/<category>/<sort>', get_publication, name='categorized_publications'),
]