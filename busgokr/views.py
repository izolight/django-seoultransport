from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from busgokr import bus

# Create your views here.
def line_search(request):
	if 'line' in request.POST:
		lines = bus.get_bus_lines(request.POST['line'])
	else:
		return HttpResponse('empty')
	template = loader.get_template('busgokr/lines.html')
	context = RequestContext(request, {
		'lines' : lines,
	})
	return HttpResponse(template.render(context))	

def index(request):
	template = loader.get_template('busgokr/index.html')
	context = RequestContext(request)
	return HttpResponse(template.render(context))