from birdsong import urls as birdsong_urls
from django.urls import include, path
from .views import subscribe

urlpatterns = [
    
    path('/', include(birdsong_urls)), 
    path('newsletter/subscribe/', subscribe, name='newsletter-subscribe'),
]