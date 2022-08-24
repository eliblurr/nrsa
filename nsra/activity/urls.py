from django.urls import include, path
from .views import categorized_page

urlpatterns = [
    path('activity-data-views/<category>/<page>/', categorized_page, name='categorized_pages'),
    # <int:category>/<int:page>/
]