import calendar
import json

from django.http import HttpResponse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, reverse
from .queries import (National_Chart, Regional, National, get_years, Categorical)


from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from json import dumps

from .data_upload_queries import *
from .data_upload_models import *
from .queries import *
from .forms import geo_data, chart_data, time_series
import logging




def index3(request):
    current_year = timezone.now().year
    calendar_html = calendar.HTMLCalendar().formatyear(current_year)

    #return HttpResponse(calendar_html)
    #return JsonResponse({"hello": "world"})
    return render(request, 'stats/index.html', {
        'N': 'National',
        'years': 'years'
    })



# logging.disable(level=logging.CRITICAL)


logging.basicConfig(filename='templog.txt', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

'''
@csrf_exempt
def index(request):
	if request.method == 'POST':
		form = geo_stats(request.POST)

		if form.is_valid():
			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			region = str(form.cleaned_data['region'])

			logging.info(f"Index method:: {date_from} | {date_to} | '{region}'")

			if region == 'ghana':
				stats_got = National(date_from, date_to)
			elif region == 'Accra':
				stats_got = Regional(date_from, date_to, 'Accra')
				stats_Tema = Regional(date_from, date_to, 'Tema')

				try:
					for k, v in stats_Tema.items():
						stats_got.update({k: stats_got[k] + v})
				except AttributeError as e:
					logging.warning(e)
			else:
				stats_got = Regional(date_from, date_to, region)

		else:
			stats_got = None

		return JsonResponse(stats_got, safe=False)

	else:
		return render(request, 'stats/charts/index.html', {
			'N': National,
			'years': years
		})


@csrf_exempt
def chart(request):
	logging.info(f" Chart method:: {request}")
	if request.method == 'POST':
		form = chart_stats(request.POST)
		if form.is_valid():
			logging.info(form.cleaned_data)

			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			category = str(form.cleaned_data['category'])
			region = str(form.cleaned_data['region'])
			specific = str(form.cleaned_data['specific'])

			if region == 'ghana' and category == 'all':
				stats_got = National_Chart(date_from, date_to, specific)
				logging.debug('ghana and all got')
			elif region != 'ghana' and category == 'all':
				stats_got = Regional(date_from, date_to, region)
				logging.debug('not ghana and all got')
			elif (region == 'ghana' and category != 'all') or (region != 'ghana' and category != 'all'):
				stats_got = Categorical(date_from, date_to, category, region)
				logging.debug('category got')
			else:
				stats_got = None
				logging.debug('nothing got')
		else:
			stats_got = None

		return JsonResponse(stats_got, safe=False)

	else:
		return render(request, 'stats/charts/charts.html', {
			'N': National,
			'years': years
		})


def common_times(request):
	form = time_series(request.POST)

	if form.is_valid():
		logging.info(form.cleaned_data)

		option: list = form.cleaned_data['option']  # must be a list/Array; even if with only one element
		stats_got = selector(option)
	else:
		stats_got = None

	return JsonResponse(stats_got, safe=False)


@csrf_exempt
def time(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		option = ['A']
		return render(request, 'stats/charts/NTF.html', {
			'stats': dumps(selector(option))
		})



@csrf_exempt
def age_group(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/age_group.html')


@csrf_exempt
def gender(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/gender.html')


@csrf_exempt
def FCE(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/FCE.html')


@csrf_exempt
def UNF(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/UNF.html')


@csrf_exempt
def UNC(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/UNC.html')


@csrf_exempt
def vehicles(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/Vehicles.html')


@csrf_exempt
def NTCC(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/NTCC.html')
'''

from django.views.decorators.clickjacking import xframe_options_exempt



@csrf_exempt
def index(request):
	if request.method == 'POST':
		form = geo_data(request.POST)

		if form.is_valid():
			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			region = str(form.cleaned_data['region'])

			logging.info(f"Index method:: {date_from} | {date_to} | '{region}'")

			if region == 'ghana':
				stats_got = National(date_from, date_to)
			elif region == 'Accra':
				stats_got = Regional(date_from, date_to, 'Accra')
				stats_Tema = Regional(date_from, date_to, 'Tema')
                #logging.info(stats_got)
				stats_Tema = Regional(date_from, date_to, 'Tema')

				try:
					for k, v in stats_Tema.items():
						stats_got.update({k: stats_got[k] + v})
				except AttributeError as e:
					logging.warning(e)
			else:
				stats_got = Regional(date_from, date_to, region)

		else:
			stats_got = None

        #print(stats_got)
		return JsonResponse(stats_got, safe=False)


	else:
		return render(request, 'stats/charts/index.html', {
			'N': National,
			'years': get_years()
		})


@csrf_exempt
def chart(request):
	logging.info(f" Chart method:: {request}")
	if request.method == 'POST':
		form = chart_data(request.POST)
		if form.is_valid():
			logging.info(form.cleaned_data)

			date_from = form.cleaned_data['date_from']
			date_to = form.cleaned_data['date_to']
			category = str(form.cleaned_data['category'])
			region = str(form.cleaned_data['region'])
			specific = str(form.cleaned_data['specific'])

			if region == 'ghana' and category == 'all':
				stats_got = National_Chart(date_from, date_to, specific)
				logging.debug(f'ghana and all got {stats_got}')
			elif region != 'ghana' and category == 'all':
				stats_got = Regional(date_from, date_to, region)
				logging.debug('not ghana and all got')
			elif (region == 'ghana' and category != 'all') or (region != 'ghana' and category != 'all'):
				stats_got = Categorical(date_from, date_to, category, region)
				logging.debug('category got')
			else:
				stats_got = None
				logging.debug('nothing got')
		else:
			stats_got = None

		return JsonResponse(stats_got, safe=False)

	else:
		return render(request, 'stats/charts/charts.html', {
			'N': National,
			'years': get_years()
		})

@csrf_exempt
def common_times(request):
	form = time_series(request.POST)

	if form.is_valid():
		logging.info(form.cleaned_data)

		option: list = form.cleaned_data['option']  # must be a list/Array; even if with only one element
		stats_got = selector(option)
	else:
		stats_got = None

	return JsonResponse(stats_got, safe=False)


@csrf_exempt
@xframe_options_exempt
def time(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		option = ['A']
		return render(request, 'stats/charts/NTF.html', {
			'stats': dumps(selector(option))
		})

@csrf_exempt
@xframe_options_exempt
def time_index(request):
	return render(request, 'stats/charts/time_series.html')


@csrf_exempt
def age_group(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/age_group.html')


@csrf_exempt
def gender(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/gender.html')


@csrf_exempt
def FCE(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/FCE.html')


@csrf_exempt
def UNF(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/UNF.html')


@csrf_exempt
def UNC(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/UNC.html')


@csrf_exempt
def vehicles(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/vehicles.html')


@csrf_exempt
def NTCC(request):
	if request.method == 'POST':
		return common_times(request)
	else:
		return render(request, 'stats/charts/NTCC.html')