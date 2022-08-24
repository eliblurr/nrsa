import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from . import spreadsheet_parser
from .data_extractor import format_1, format_2
from standard_data.standard_extractor import main
from data_upload.forms import upload_data


def upload(request):

	if request.method == 'POST':

		form = upload_data(request.POST, request.FILES)

		if form.is_valid():

			option = form.cleaned_data['option']

			def file_handler(file):
				logging.info(dir(file))
				csv_str = spreadsheet_parser.file_ext_check(file)
				return csv_str

			if option == 'First':
				CSV = file_handler(request.FILES['file'])
				format_1(CSV)
			elif option == 'Second':
				filename = '.'.join(request.FILES['file'].name.split('.')[:-1])
				logging.info(f"{filename} Received")
				format_2(request.FILES['file'], filename)
			elif option == 'Standard':
				filename = '.'.join(request.FILES['file'].name.split('.')[:-1])
				logging.info(f"{filename} Received")
				main(request.FILES['file'], filename)

			return HttpResponseRedirect("admin")
		else:
			return HttpResponseRedirect('File upload Failed')

	else:
		form = upload_data()

	return render(request, 'data_upload/upload.html', {'form': form})