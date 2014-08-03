import logging

from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext, loader

from busgokr.models import BusRoute, SearchedLive, BusStation, Sequence
from busgokr.utils import search_bus_live, add_line_to_db, get_stations_by_line, search_stations_live, add_segment_to_db


logger = logging.getLogger(__name__)

RESULT_LIST = 'resultList'
BUS_LIST = 'busList'


def update_lines(request):
    search = request.POST['search']
    live_lines = search_bus_live(search)
    if RESULT_LIST in live_lines:
        live_lines = live_lines[RESULT_LIST]
        for line in live_lines:
            add_line_to_db(line)
    lines = BusRoute.objects.filter(name__contains=search).order_by('route_type', 'name')
    context = RequestContext(request, {
        'lines': lines,
        'search': search,
    })
    template = loader.get_template('busgokr/lines_all.html')

    return HttpResponse(template.render(context))


def all_lines(request):
    if request.method == 'POST' and 'search' in request.POST:
        return HttpResponseRedirect(request.POST['search'] + '/')
    lines = BusRoute.objects.all()
    context = RequestContext(request, {
        'lines': lines,
    })

    template = loader.get_template('busgokr/lines_all.html')

    return HttpResponse(template.render(context))

def search_lines(request, query):
    search = query
    lines = BusRoute.objects.filter(name__contains=search).order_by('route_type', 'name')
    context = RequestContext(request, {
        'lines': lines,
        'search': search,
    })
    template = loader.get_template('busgokr/lines_all.html')

    return HttpResponse(template.render(context))

def search_stations(request):
    if request.method == 'POST' and 'search' in request.POST:
        search = request.POST['search']
        stations = BusStation.objects.filter(name__contains=search)
        context = RequestContext(request, {
            'stations': stations,
            'search': search,
        })
    else:
        stations = BusStation.objects.all()
        context = RequestContext(request, {
            'stations': stations,
        })

    template = loader.get_template('busgokr/stations_all.html')

    return HttpResponse(template.render(context))


def line_detail(request, line_id):
    busroute = BusRoute.objects.get(id=line_id)
    try:
        SearchedLive.objects.get(busroute=busroute)
    except SearchedLive.DoesNotExist:
        segments = get_stations_by_line(line_id)
        segments = segments[RESULT_LIST]
        for segment in segments:
            add_segment_to_db(segment)
        SearchedLive(busroute=busroute).save()

    segments = Sequence.objects.filter(route=busroute).order_by('number')


    template = loader.get_template('busgokr/line_detail.html')
    context = RequestContext(request, {
        'segments': segments,
    })
    return HttpResponse(template.render(context))


def station_detail(request, station_name):
    if request.method == 'POST' and 'search' in request.POST:
        search = request.POST['search']
        stations = search_stations_live(search)
    else:
        stations = search_stations_live(station_name)
    stations = stations[BUS_LIST]

    template = loader.get_template('busgokr/station_detail.html')
    context = RequestContext(request, {
        'stations': stations,
    })
    return HttpResponse(template.render(context))