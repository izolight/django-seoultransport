import logging

from django.http import HttpResponse

from django.template import RequestContext, loader

from busgokr.models import BusRoute, SearchedLive
from busgokr.utils import search_live, add_line_to_db, get_stations_by_line


logger = logging.getLogger(__name__)

RESULT_LIST = 'resultList'


def index(request):
    template = loader.get_template('busgokr/index.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def search_lines(request):
    if request.method == 'POST':
        if 'search' in request.POST:
            search = request.POST['search']
            searched_before = SearchedLive.objects.filter(busroute=search)
            if not searched_before:
                live_lines = search_live(search)
                if RESULT_LIST in live_lines:
                    live_lines = live_lines[RESULT_LIST]
                    for line in live_lines:
                        add_line_to_db(line)
                SearchedLive(busroute=search).save()
            lines = BusRoute.objects.filter(name__contains=search).order_by('route_type', 'name')
            context = RequestContext(request, {
                'lines': lines,
                'search': search,
            })
    elif request.method == 'GET':
        lines = BusRoute.objects.all()
        context = RequestContext(request, {
            'lines': lines,
        })

    template = loader.get_template('busgokr/lines_all.html')

    return HttpResponse(template.render(context))


def line_detail(request, line_id):
    stations = get_stations_by_line(line_id)
    stations = stations[RESULT_LIST]
    template = loader.get_template('busgokr/line_detail.html')
    context = RequestContext(request, {
        'stations': stations,
    })
    return HttpResponse(template.render(context))
