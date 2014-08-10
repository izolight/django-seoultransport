import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import RequestContext, loader

from busgokr.models import *
from busgokr.utils import search_bus_live, add_line_to_db, get_stations_by_line, add_segment_to_db


logger = logging.getLogger(__name__)

RESULT_LIST = 'resultList'
BUS_LIST = 'busList'


def update_segments(request):
    busroutes = BusRoute.objects.all()
    for route in busroutes:
        try:
            SearchedLive.objects.get(busroute=route)
        except SearchedLive.DoesNotExist:
            segments = get_stations_by_line(route.id)
            segments = segments[RESULT_LIST]
            for segment in segments:
                add_segment_to_db(segment)
            SearchedLive(busroute=route).save()
    return redirect('/busgokr/lines/')


def update_lines(request):
    search = ''
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
    template = loader.get_template('busgokr/lines.html')

    return HttpResponse(template.render(context))


def all_lines(request):
    if request.method == 'POST' and 'search' in request.POST:
        return HttpResponseRedirect(request.POST['search'] + '/')
    lines = BusRoute.objects.all()[:100]
    context = RequestContext(request, {
        'lines': lines,
    })

    template = loader.get_template('busgokr/lines.html')

    return HttpResponse(template.render(context))


def search_lines(request, query):
    search = query
    lines = BusRoute.objects.filter(name__contains=search).order_by('route_type', 'name')
    context = RequestContext(request, {
        'lines': lines,
        'search': search,
    })
    template = loader.get_template('busgokr/lines.html')

    return HttpResponse(template.render(context))


def all_locations(request):
    if request.method == 'POST' and 'search' in request.POST:
        return HttpResponseRedirect(request.POST['search'] + '/')
    locations = Location.objects.all()[:100]
    context = RequestContext(request, {
        'locations': locations,
    })

    template = loader.get_template('busgokr/locations.html')

    return HttpResponse(template.render(context))


def search_locations(request, query):
    search = query
    locations = Location.objects.filter(name__icontains=search)
    context = RequestContext(request, {
        'locations': locations,
        'search': search,
    })
    template = loader.get_template('busgokr/locations.html')

    return HttpResponse(template.render(context))


def line_detail(request, line_id):
    busroute = BusRoute.objects.get(id=line_id)
    try:
        SearchedLive.objects.get(busroute=busroute)
    except SearchedLive.DoesNotExist:
        segments = get_stations_by_line(line_id)
        logger.error(len(segments))
        if RESULT_LIST in segments != "None":
            segments = segments[RESULT_LIST]
            for segment in segments:
                add_segment_to_db(segment)
        SearchedLive(busroute=busroute).save()

    segments = Sequence.objects.filter(route=busroute).order_by('number')
    distance = 0
    iterseg = iter(segments)
    next(iterseg)
    for segment in iterseg:
        distance += segment.section.distance

    template = loader.get_template('busgokr/line_detail.html')
    context = RequestContext(request, {
        'segments': segments,
        'distance': distance,
        'line': busroute,
    })
    return HttpResponse(template.render(context))


def station_detail(request, station_id):
    station = BusStation.objects.get(id=station_id)
    sequences = Sequence.objects.filter(station=station)
    template = loader.get_template('busgokr/station_detail.html')
    context = RequestContext(request, {
        'station': station,
        'sequences': sequences,
    })
    return HttpResponse(template.render(context))


def directions(request, direction):
    search = direction
    location = Location.objects.get(name=search)
    sequences = Sequence.objects.filter(direction=location)
    lines = []
    for s in sequences:
        line = s.route
        if line not in lines:
            lines.append(s.route)
    context = RequestContext(request, {
        'lines': lines,
        'search': search,
    })
    template = loader.get_template('busgokr/lines.html')

    return HttpResponse(template.render(context))


def corporations(request, corp_id):
    corporation = Corporation.objects.get(id=corp_id)
    lines = BusRoute.objects.filter(corporation=corporation)
    context = RequestContext(request, {
        'lines': lines,
    })

    template = loader.get_template('busgokr/lines.html')

    return HttpResponse(template.render(context))


def location_detail(request, loc_id):
    location = Location.objects.get(id=loc_id)
    stations = BusStation.objects.filter(name=location)
    context = RequestContext(request, {
        'stations': stations,
    })

    template = loader.get_template('busgokr/location_detail.html')

    return HttpResponse(template.render(context))