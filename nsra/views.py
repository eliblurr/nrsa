from django.shortcuts import render, reverse

def unauthorized(request):
	return render(request, '401.html')


# from django.shortcuts import render_to_response
# from django.template import RequestContext

# # HTTP Error 400
# def bad_request(request):
#     response = render_to_response(
#         '400.html',
#         context_instance=RequestContext(request)
#     )

#     response.status_code = 400
#     return response

from django.shortcuts import render

def handle404(request, exception=None):
	home = request.scheme + '://' + request.get_host()
	response = render(request, '404.html', context={'home':home})
	response.status_code = 404
	return response

def handle400(request, exception=None):
	home = request.scheme + '://' + request.get_host()
	response = render(request, '400.html', context={'home':home})
	response.status_code = 400
	return response

def handle403(request, exception=None):
	home = request.scheme + '://' + request.get_host()
	response = render(request, '403.html', context={'home':home})
	response.status_code = 403
	return response

def handle500(request):
	home = request.scheme + '://' + request.get_host()
	response = render(request, '500.html', context={'home':home})
	response.status_code = 500
	return response