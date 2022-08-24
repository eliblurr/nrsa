#from . views import index
from . import views

from django.urls import path

app_name = 'stats'

urlpatterns = [
    #path('', views.index, name="index_view"),
    path('', views.index, name='index'),

    path('NTF/', views.time, name='NTF'),
	path('time/series/index/', views.time_index, name='time_series'),
	path('chart/', views.chart, name='chart'),
	path('age_group/', views.age_group, name='age_group'),
	path('gender/', views.gender, name='gender'),
	path('FCE/', views.FCE, name='FCE'),
	path('UNF/', views.UNF, name='UNF'),
	path('UNC/', views.UNC, name='UNC'),
	path('vehicles/', views.vehicles, name='vehicles'),
	path('NTCC/', views.NTCC, name='NTCC'),

]